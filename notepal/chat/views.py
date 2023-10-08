from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from note.models import NoteFileembedding
from chat.models import History
import mistletoe


@login_required
def chat(request):
    note_embedding = NoteFileembedding.objects.filter(owner=request.user)
    chat_history = History.objects.filter(user_owner=request.user)

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
        "chat_length": len(chat_history),
        "chat_history": chat_history_list,
        "notes": note_embedding,
    }

    return render(request, "chat.html", context)
