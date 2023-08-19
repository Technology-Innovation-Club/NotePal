import openai
import os
import tiktoken
from pgvector.django import CosineDistance
from note.load_file import get_vector
from chat.models import NoteEmbedding

# implement the quiz feature
SYSTEM_CONTENT = """
you are a students assistant. 
Use the current reference document to improve the current response to the users question. The output should be a response that is easy for the student to understand. 
The format of the response should be in markdown format when required to boost the students understanding of the response. The response should also be to the point and not contain unnecessary information.
"""

QUIZ = """"
When a user requests to be tested or quizzed, analyze both the question posed by the user. 
Utilize this information to formulate appropriate questions for assessing the user's knowledge. 
Determine the optimal number of questions to present and set the difficulty level of these questions based on the user's proficiency. 
Additionally, choose the appropriate question format based on the content: for theoretical questions, 
prompt the user to type out their answer, whereas for objective questions, provide multiple-choice options.
The output of this process should be presented in JSON format, comprising the following elements:
'question': The formulated question for the user.
'type_of_question': This field indicates whether the question is theoretical ('theory') or objective ('objective').
'options' (Only for objective questions): A list of multiple-choice options for the user to choose from.
'the_answer' (Only for objective questions): The correct answer, which should match one of the provided options."""

# openai.api_key_path='/code/.env'
# config = dotenv.dotenv_values(".env")
openai.api_key = "<your openai api key>"
distance_limit = 5


def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
    }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif "gpt-3.5-turbo" in model:
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def get_completion_stuff(msgs, model="gpt-3.5-turbo", temperature=0.7):
    response = openai.ChatCompletion.create(
        model=model,
        messages=msgs,
        temperature=temperature,
    )
    # print(f"The number of items in messages: {len(msgs)}")
    # print(f"The tokens: {num_tokens_from_messages(msgs)}")
    # print(f"The response is: {response}")
    return response


context = [
    {
        "role": "system",
        "content": SYSTEM_CONTENT,
    }
]


def ask_question_stuff(query):
    update_db = {}
    update_db["user_question"] = query
    query_vector = get_vector(query)
    
    results = NoteEmbedding.objects.alias(
        distance=CosineDistance("vector", query_vector)
    ).filter(distance__lt=0.5)[:3]
    texts = ""
    update_db["embedding_text"] = [result.file_text for result in results]  
    update_db["embedding_context"] = [
        {"id": result.id, "text": result.file_text} for result in results
    ]
    update_db["llm_algo_used"] = "gpt-3.5-turbo"
    for result in results:
        text = result.file_text + ".\n"
        texts += text
    # texts = results.text

    # print(texts)
    context.append(
        {
            "role": "system",
            "content": f"referencing this document: {texts}",
        }
    )
    context.append(
        {
            "role": "system",
            "content": f"Ignore the context document and do not reference it in your response if it does not apply to the question.",
        }
    )
    context.append(
        {
          "role": "system",
            "content": QUIZ, 
        })
    context.append(
        {
            "role": "user",
            "content": f"Answer the question {query}",
        }
    )
    response = get_completion_stuff(context)
    update_db["response"] = response.choices[0].message["content"]
    update_db["response_to_user"] = response.choices[0].message["content"]
    context.append({"role": "assistant", "content": response})
    # only set in multiples of 2
    if len(context) > 6:
        context.pop()
        context.pop()
    if num_tokens_from_messages(context) > 4000:
        context.pop()
        context.pop()
    update_db["question_dict"] = context
    # return response.choices[0].message["content"]
    return update_db
