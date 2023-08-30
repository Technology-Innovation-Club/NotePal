from ninja import Router, File, Schema, Form
from ninja.files import UploadedFile
from .load_file import store_file, store_file_embedding
from .metadata import get_file_name, get_metadata
from note.models import NoteFileembedding
import traceback
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja.security import django_auth
from ninja.errors import HttpError

note_router = Router()


# upload a file
@note_router.post("/upload", auth=django_auth)
def file_upload(request, file: UploadedFile = File(...)):
    if request.user.is_authenticated:
        user_email = request.user.email
        try:
            file_name = get_file_name(file.name)
            metadata = get_metadata(file)
            
            note_file = store_file(file.read(), file_name, metadata, user_email)

            try:
                # store note chunks and embeddings
                store_file_embedding(note_file)
            except Exception as e:
                NoteFileembedding.objects.filter(id=note_file.id).delete()
                return e

            return note_file.id
        except Exception:
            print(traceback.format_exc())
            return Exception
    else:
        error = {}
        error["error"] = "User not authenticated"
        raise HttpError(401, message=error)

# get all users uploaded files
@note_router.get("/all", auth=django_auth)
def get_all(request):
    if request.user.is_authenticated:
        output = {}
        user = get_object_or_404(User, username=request.user.username)
        note_files = NoteFileembedding.objects.filter(owner=user)
        output["files"] = [note_file.name for note_file in note_files]
        return output["files"]
    else:
        error = {}
        error["error"] = "User not authenticated"
        raise HttpError(401, message=error)


# remove a users specific file
@note_router.delete("/remove", auth=django_auth)
def remove(request, filename: str):
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.username)
        note = get_object_or_404(NoteFileembedding, name=filename, owner=user)
        note.delete()
        return f"{filename} has been removed"
    else:
        error = {}
        error["error"] = "User not authenticated"
        raise HttpError(401, message=error)
