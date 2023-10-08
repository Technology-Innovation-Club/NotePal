import openai

# import os
import tiktoken
from pgvector.django import CosineDistance
from note.load_file import get_vector
from chat.models import NoteEmbedding

# from chat.quiz import quiz_notify
# import json
import os
from users.models import NotepalUser

# from note.load_file import process_quiz_data


# system with quiz
# SYSTEM_CONTENT = """
# you are a students assistant.
# Use the current reference document to improve the current response to the users question. The output should be a response that is easy for the student to understand.
# Always show your answer in markdown format to boost the students understanding of the response, it should also be appropriately structured and spaced. The response should also be to the point and not contain unnecessary information.
# Ignore the context document and do not reference it in your response if it does not apply to the question.
# ALWAYS use the functions to find a function to trigger quizzes when a user asks for a quiz, test, questions or any form test of knowledge in anyway manner it is asked.
# """
SYSTEM_CONTENT = """
you are a students assistant. 
Use the current reference document to improve the current response to the users question. The output should be a response that is easy for the student to understand. 
Always show your answer in markdown format to boost the students understanding of the response, it should also be appropriately structured and spaced. The response should also be to the point and not contain unnecessary information.
Ignore the context document and do not reference it in your response if it does not apply to the question.  
"""


def get_api_key(user):
    notepal_user = NotepalUser.objects.get(user=user)
    api_key = notepal_user.api_key
    return api_key


from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


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


# functions = [
#     {
#         "name": "quiz_notify",
#         "description": "Useful for outputting a quiz to the user.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "user_message": {
#                     "type": "string",
#                     "description": "The users question",
#                 },
#             },
#             "required": ["user_message"],
#         },
#     }
# ]


def get_completion_stuff(user, msgs, model="gpt-3.5-turbo", temperature=0.7):
    openai.api_key = get_api_key(user)
    response = openai.ChatCompletion.create(
        model=model,
        messages=msgs,
        temperature=temperature,
        # functions=functions,
        # function_call="auto",  # auto is default, but we'll be explicit
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


def ask_question_stuff(user, query):
    update_db = {}
    update_db["user_question"] = query
    query_vector = get_vector(query)

    results = NoteEmbedding.objects.alias(
        distance=CosineDistance("vector", query_vector)
    ).filter(distance__lt=0.5)[:3]
    texts = ""
    embedding_text_temp = []
    for result in results:
        embedding_text_temp.append({"id": result.id, "text": result.file_text})
    update_db["query_context"] = embedding_text_temp

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
            "role": "user",
            "content": f"Answer the question {query}",
        }
    )
    response = get_completion_stuff(user, context)
    response_message = response["choices"][0]["message"]
    # if response_message.get("function_call"):
    #     available_functions = {
    #         "quiz_notify": quiz_notify,
    #     }
    #     function_name = response_message["function_call"]["name"]
    #     function_to_call = available_functions[function_name]
    #     function_args = json.loads(response_message["function_call"]["arguments"])
    #     function_response = function_to_call(
    #         user_message=function_args["user_message"],
    #     )
    #     # context.append(response_message)
    #     context.append(
    #         {
    #             "role": "function",
    #             "name": function_name,
    #             "content": str(function_response),
    #         }
    #     )
    #     # second_response = openai.ChatCompletion.create(
    #     #     model="gpt-3.5-turbo",
    #     #     messages=context,
    #     # )
    #     response = function_response
    #     print(f"function response: {response.choices[0].message['content']}")

    #     update_db["response"] = response.choices[0].message["content"]
    #     # change to JSON
    #     temp_json_data = json.loads(response.choices[0].message["content"])
    #     update_db["response_to_user"] = process_quiz_data(user, temp_json_data)
    #     context.append(
    #         {"role": "assistant", "content": response.choices[0].message["content"]}
    #     )
    #     # only set in multiples of 2
    #     # if len(context) > 10:
    #     #     context.pop()
    #     #     context.pop()
    #     if num_tokens_from_messages(context) > 4000:
    #         context.pop()
    #         context.pop()
    #     return update_db

    update_db["response"] = response.choices[0].message["content"]
    # change to JSON
    update_db["response_to_user"] = response.choices[0].message["content"]
    print(f"response: {response.choices[0].message['content']}")
    context.append(
        {"role": "assistant", "content": response.choices[0].message["content"]}
    )
    # only set in multiples of 2
    # if len(context) > 10:
    #     context.pop()
    #     context.pop()
    if num_tokens_from_messages(context) > 4000:
        context.pop()
        context.pop()
    return update_db
