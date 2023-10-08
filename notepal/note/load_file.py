from langchain.text_splitter import RecursiveCharacterTextSplitter

# from load_file import
from note.models import NoteFileembedding
from chat.models import NoteEmbedding
from django.utils import timezone
import io
from numpy import ndarray
from sentence_transformers import SentenceTransformer
from .handle_file import (
    upload_docx_file,
    upload_pdf_file,
    upload_pptx_file,
    get_docx_text,
    get_pptx_text,
    get_pdf_text,
)
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, HttpResponse
from chat.models import History
from ninja.errors import HttpError
import markdown
from xhtml2pdf import pisa
import tempfile
import os
import zipfile
from ninja import Schema

model = SentenceTransformer("all-MiniLM-L6-v2")


def get_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True,
    )
    split_texts = text_splitter.create_documents([text])
    return split_texts


def get_vector(text) -> ndarray:
    vector = model.encode(text)
    return vector


def handle_upload(file, file_type):
    if file_type == "pdf":
        pdf_reader = upload_pdf_file(file)
        return get_pdf_text(pdf_reader)
    elif file_type == "docx":
        docx_reader = upload_docx_file(file)
        return get_docx_text(docx_reader)
    elif file_type == "pptx":
        pptx_file = upload_pptx_file(file)
        return get_pptx_text(pptx_file)
    else:
        return None


def read_file(file_embedding: NoteFileembedding):
    file = file_embedding.the_file
    file_decode = io.BytesIO(file)
    output_text = handle_upload(file_decode, file_embedding.metadata["file_type"])
    return output_text


def store_file(file, filename, metadata, email):
    owner = get_object_or_404(User, email=email)
    note_file = NoteFileembedding.objects.create(
        owner=owner,
        name=filename,
        the_file=file,
        metadata=metadata,
        date_created=timezone.now(),
        date_updated=timezone.now(),
    )
    # add_to_history
    History.objects.create(user_owner=owner, file_uploaded=note_file)

    return note_file

def store_pdf_file_history(email,file):
    owner = get_object_or_404(User, email=email)
    store_pdf = History.objects.create(user_owner=owner, the_file=file)
    return store_pdf


def store_file_embedding(file_embedding):
    text = read_file(file_embedding)
    chunks = get_chunks(text)
    for i in range(len(chunks)):
        chunk = chunks[i].page_content
        vector = get_vector(chunk)
        NoteEmbedding.objects.create(
            file_text=chunk,
            file_embedding=file_embedding,
            vector=vector,
            date_created=timezone.now(),
        )

# 


def process_quiz_data(user, quizDetails):
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
        store_pdf_file_history(user.email, combined_pdf_bytes)
        
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
