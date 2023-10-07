from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from note.models import NoteFileembedding
from chat.models import History
import mistletoe
from django.shortcuts import get_object_or_404

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
            "file_name": "Quiz data" if entry.the_file is not None else (entry.file_uploaded.name if entry.file_uploaded else None),
            "file_data": True if entry.the_file is not None else False
        }
        chat_history_list.append(chat_history_item)

    context = {
        "chat_length": len(chat_history),
        "chat_history": chat_history_list,
        "notes": note_embedding,
    }

    return render(request, "chat.html", context)

def download_file(request, history_id):
    # Retrieve the History object
    history_entry = get_object_or_404(History, user_owner=request.user, id=history_id)

    # Ensure the user has permission to access the file if needed
    # (e.g., check if the user is the owner of the file)

    # Set the response headers for file download
    response = FileResponse(history_entry.the_file, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="quiz_data.zip"'

    return response