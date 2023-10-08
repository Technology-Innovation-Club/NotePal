from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from note.models import NoteFileembedding
from chat.models import History
from users.models import NotepalUser
import mistletoe


@login_required
def chat(request):
    user_embedding = NotepalUser.objects.filter(user=request.user).first() 
    note_embedding = NoteFileembedding.objects.filter(owner=request.user)
    chat_history = History.objects.filter(user_owner=request.user)
    
    api_key = user_embedding.api_key if user_embedding.api_key != "" else ""
    
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
    

    context = {
        "api_key": api_key,
        "chat_length": len(chat_history),
        "chat_history": chat_history_list,
        "notes": note_embedding,
    }

    return render(request, "chat.html", context)
