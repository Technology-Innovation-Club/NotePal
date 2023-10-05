from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from note.models import NoteFileembedding

@login_required
def chat(request):
    note_embedding = NoteFileembedding.objects.filter(owner=request.user)
    # user_email = request.user.email
    context = {
        'notes': note_embedding,
    }
    return render(request, "chat.html", context)

