from django.db import models
from django.contrib.auth.models import User
from django_cryptography.fields import encrypt
import uuid


class NotepalUser(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="notepaluser"
    )
    api_key = encrypt(models.CharField(max_length=255, default=uuid.uuid4))
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    # objects = UserManager()
