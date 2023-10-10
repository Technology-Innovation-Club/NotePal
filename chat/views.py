from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from note.models import NoteFileembedding
from chat.models import History
from users.models import NotepalUser
import mistletoe
import uuid
from django.utils import timezone
from django.contrib.auth import login

# Create a demo user
def create_demo_user(request):
    username = f"demo_{uuid.uuid4()}"
    password = User.objects.make_random_password()
    user = User.objects.create_user(username, password)
    user.is_active = True
    user.save()

    # Set the expiration date for the user's session to 1 hour.
    request.session.set_expiry(timezone.now() + timezone.timedelta(days=1))

    login(request, user)

    return redirect("chat")


def chat(request):
    # Get the user's embedding.
    user_embedding = NotepalUser.objects.filter(user=request.user).first()

    # Get the user's note embeddings.
    note_embedding = NoteFileembedding.objects.filter(owner=request.user)

    # Get the user's chat history.
    chat_history = History.objects.filter(user_owner=request.user)

    # Get the user's API key.
    api_key = user_embedding.api_key if user_embedding.api_key != "" else ""

    # Create a list of the user's chat history items.
    chat_history_list = []
    for entry in chat_history:
        chat_history_item = {
            "question": entry.user_question,
            "response": mistletoe.markdown(entry.response_to_user)
            if entry.response_to_user is not None
            else None,
            "file_name": entry.file_uploaded.name if entry.file_uploaded else None,
        }
        chat_history_list.append(chat_history_item)

    # Create the context for the chat template.
    context = {
        "api_key": api_key,
        "chat_length": len(chat_history),
        "chat_history": chat_history_list,
        "notes": note_embedding,
    }

    # Return an HttpResponse object.
    return render(request, "chat.html", context)
