from ninja import Router
from chat.query_embedding import ask_question_stuff
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from chat.models import History
from ninja.security import django_auth


chat_router = Router()


# query chatbot
@chat_router.post("/query", auth=django_auth)
def query(request, query: str):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        response = ask_question_stuff(query)
        if len(response["query_context"]) > 0:
            user_question = response["user_question"]
            embedding_context = response["query_context"]
            llm_algo_used = response["llm_algo_used"]
            response_to_user = response["response_to_user"]
            llm_response = response["response"]
            user_id = user

            # save to table
            History.objects.create(
                user_id=user_id,
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
                user_id=user_id,
                user_question=user_question,
                llm_response=llm_response,
                response_to_user=response_to_user,
                llm_algo_used=llm_algo_used,
            )
            return response["response_to_user"]

# getting the history of the user
# adding the history into context
@chat_router.get("/history", auth=django_auth)
def history(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        history_collection = History.objects.filter(user_id=user)
        output = {}
        output["history"] = [
            {
                "user_question": history.user_question,
                "llm_response": history.llm_response,
                "response_to_user": history.response_to_user,
                "llm_algo_used": history.llm_algo_used,
                "embedding_context": history.embedding_context,
            }
            for history in history_collection
        ]
        return output["history"]

# clearing chat history
@chat_router.delete("/clear", auth=django_auth)
def clear(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        history_collection = History.objects.filter(user_id=user)
        history_collection.delete()
        return "History cleared"