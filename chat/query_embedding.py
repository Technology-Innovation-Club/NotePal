import openai
import tiktoken
from pgvector.django import CosineDistance
from note.load_file import get_vector
from chat.models import NoteEmbedding
from users.models import NotepalUser


SYSTEM_CONTENT = """
you are a students assistant. 
Use the current reference document to improve the current response to the users question. The output should be a response that is easy for the student to understand. 
Always show your answer in markdown format to boost the students understanding of the response, it should also be appropriately structured and spaced. The response should also be to the point and not contain unnecessary information.
Ignore the context document and do not reference it in your response if it does not apply to the question.  
"""

# Get the OpeNAI key
def get_api_key(user):
    notepal_user = NotepalUser.objects.get(user=user)
    api_key = notepal_user.api_key
    return api_key


from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


distance_limit = 5

# Get the number of tokens in context
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

def get_completion_stuff(user, msgs, model="gpt-3.5-turbo", temperature=0.7):
    openai.api_key = get_api_key(user)
    response = openai.ChatCompletion.create(
        model=model,
        messages=msgs,
        temperature=temperature,
    )
    return response


context = [
    {
        "role": "system",
        "content": SYSTEM_CONTENT,
    }
]

# Process users request
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

    update_db["response"] = response.choices[0].message["content"]
    update_db["response_to_user"] = response.choices[0].message["content"]
    context.append(
        {"role": "assistant", "content": response.choices[0].message["content"]}
    )

    if num_tokens_from_messages(context) > 4000:
        context.pop()
        context.pop()
    return update_db
