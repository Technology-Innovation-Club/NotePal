from django.db import models
from django.contrib.auth.models import User
import uuid


class NotepalUser(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="notepaluser"
    )
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    # objects = UserManager()
