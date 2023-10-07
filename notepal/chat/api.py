from ninja import Router, File, Schema, Form
from chat.query_embedding import ask_question_stuff
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from chat.models import History
from ninja.security import django_auth
from ninja.errors import HttpError
import markdown
from xhtml2pdf import pisa
from note.load_file import store_pdf_file_history
import tempfile
import os
import zipfile


chat_router = Router()


class questionSchema(Schema):
    query: str

class quizSchema(Schema):
    questions: list[str]
    type_of_question: list[str]
    options: list[list]
    the_answer: list[str]

# query chatbot
@chat_router.post("/query", auth=django_auth)
def query(request, queryDetails: questionSchema = Form(...)):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        response = ask_question_stuff(request.user, queryDetails.query)
        if len(response["query_context"]) > 0:
            user_question = response["user_question"]
            embedding_context = response["query_context"]
            llm_algo_used = response["llm_algo_used"]
            response_to_user = response["response_to_user"]
            llm_response = response["response"]
            user_id = user

            # save to table
            History.objects.create(
                user_owner=user_id,
                user_question=user_question,
                llm_response=llm_response,
                response_to_user=response_to_user,
                llm_algo_used=llm_algo_used,
                embedding_context=embedding_context,
            )
            return response["response_to_user"]
        else:
            user_question = response["user_question"]
            llm_algo_used = response["llm_algo_used"]
            response_to_user = response["response_to_user"]
            llm_response = response["response"]
            user_id = user

            History.objects.create(
                user_owner=user_id,
                user_question=user_question,
                llm_response=llm_response,
                response_to_user=response_to_user,
                llm_algo_used=llm_algo_used,
            )
            return response["response_to_user"]
    else:
        error = {}
        error["error"] = "User not authenticated"
        raise HttpError(401, message=error)



@chat_router.post("/quiz-data", auth=django_auth)
def process_quiz_data(request, quizDetails: quizSchema):
    if request.user.is_authenticated:
        # Convert the quiz data to Markdown format
        questions_markdown = "# Practice questions\n\n"
        answers_markdown = "# Practice answers\n\n"

        for i, question in enumerate(quizDetails.questions):
            # Add the question number to the beginning of the question
            questions_markdown += f"{i + 1}. {question}\n"

            if quizDetails.type_of_question[i] == "objective":
                # Add the answer options to the question
                for option in quizDetails.options[i]:
                    questions_markdown += f"    * {option}\n"

            # Add the answer to the answers Markdown file
            answers_markdown += f"{i + 1}. {quizDetails.the_answer[i]}\n"

        # Convert Markdown to HTML for questions
        questions_html_content = markdown.markdown(questions_markdown)

        # Convert Markdown to HTML for answers
        answers_html_content = markdown.markdown(answers_markdown)

        # Create a temporary file to write the questions PDF
        temp_questions_file_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=True).name
        
        result_questions_file = open(temp_questions_file_path, "w+b")
        
        # convert questions HTML to PDF
        pisa.CreatePDF(
            questions_html_content,
            dest=result_questions_file,
        )
        
        result_questions_file.close()

        # Create a temporary file to write the answers PDF
        temp_answers_file_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=True).name
        
        result_answers_file = open(temp_answers_file_path, "w+b")
        
        # convert answers HTML to PDF
        pisa.CreatePDF(
            answers_html_content,
            dest=result_answers_file,
        )
        
        result_answers_file.close()

        # Open the temporary files in binary mode and read the bytes
        with open(temp_questions_file_path, "rb") as f_questions, open(temp_answers_file_path, "rb") as f_answers:
            questions_pdf_bytes = f_questions.read()
            answers_pdf_bytes = f_answers.read()
            
        # Combine both PDFs into a single binary file
        combined_pdf_bytes = questions_pdf_bytes + answers_pdf_bytes
        
        # store file in chat history
        store_pdf_file_history(request.user.email, combined_pdf_bytes)
        
        # Delete the temporary files
        os.remove(temp_questions_file_path)
        os.remove(temp_answers_file_path)

        # Create a ZIP archive containing both PDFs
        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=quiz_data.zip"

        # Create a ZIP file in memory
        with zipfile.ZipFile(response, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("questions.pdf", questions_pdf_bytes)
            zipf.writestr("answers.pdf", answers_pdf_bytes)
            
        
        return response
    else:
        error = {}
        error["error"] = "User not authenticated"
        raise HttpError(401, message=error)