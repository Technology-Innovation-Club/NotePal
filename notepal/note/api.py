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
from .validate_file import validate_uploaded_file
from users.models import NotepalUser
from ninja import Schema


note_router = Router()


class ApiKeySchema(Schema):
    api_key: str

# upload a file
@note_router.post("/upload", auth=django_auth)
def file_upload(request, file: UploadedFile = File(...)):
    if request.user.is_authenticated:
        user_email = request.user.email
        if not validate_uploaded_file(file, user_email):
            return validate_uploaded_file(file, user_email)
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
        user = get_object_or_404(User, email=request.user.email)
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

@note_router.post("/add-api-key", auth=django_auth)
def add_api_key(request, APIKEY: ApiKeySchema = Form(...)):
    owner = get_object_or_404(User, email=request.user.email)
    if request.user.is_authenticated:
        try:
            notepal_user = get_object_or_404(NotepalUser,user=owner)
            notepal_user.api_key = APIKEY.api_key
            notepal_user.save()
            return {"message": "API key added successfully"}
        except NotepalUser.DoesNotExist:
            return {"message": "NotepalUser does not exist"}
    else:
        error = {}
        error["error"] = "User not authenticated"
        raise HttpError(401, message=error)


@note_router.post("/remove-api-key", auth=django_auth)
def remove_api_key(request):
    owner = get_object_or_404(User, email=request.user.email)
    if request.user.is_authenticated:
        try:
            notepal_user = get_object_or_404(NotepalUser, user=owner)
            notepal_user.api_key = ''
            notepal_user.save()
            return {"message": "API key removed successfully"}
        except NotepalUser.DoesNotExist:
            return {"message": "NotepalUser does not exist"}
    else:
        error = {}
        error["error"] = "User not authenticated"
        raise HttpError(401, message=error)


@note_router.get("/view-api-key", auth=django_auth)
def view_api_key(request):
    owner = get_object_or_404(User, email=request.user.email)
    if request.user.is_authenticated:
        try:
            notepal_user = get_object_or_404(NotepalUser, user=owner)
            api_key = notepal_user.api_key
            return {"api_key": api_key}
        except NotepalUser.DoesNotExist:
            return {"message": "NotepalUser does not exist"}
    else:
        error = {}
        error["error"] = "User not authenticated"
        raise HttpError(401, message=error)