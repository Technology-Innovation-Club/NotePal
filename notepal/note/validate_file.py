from .metadata import get_file_name
from note.models import NoteFileembedding
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


# validate file upload
def validate_uploaded_file(file, user):
    error = {}
    owner = get_object_or_404(User, email=user)
    
    # Get the file name from the uploaded file
    file_name = get_file_name(file.name)
    
    # Check if a file with the same name already exists and is associated with the user
    existing_file = NoteFileembedding.objects.filter(name=file_name, owner=owner).first()
    if existing_file:
        error["File error"] = "File with the same name already exists."
        raise HttpError(409, message=error)

    # Check if the file type is allowed (pptx, docx, or pdf)
    allowed_file_types = ["application/vnd.openxmlformats-officedocument.presentationml.presentation", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/pdf"]
    if file.content_type not in allowed_file_types:
        error["File error"] = "Invalid file type. Only pptx, docx, and pdf files are allowed."
        raise HttpError(400, message=error)

    # If all checks pass, return True
    return True
