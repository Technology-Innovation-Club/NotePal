from django.db import models
import uuid
from django.contrib.auth.models import User


# Table to store the users note
class NoteFileembedding(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    name = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    the_file = models.BinaryField()
    metadata = models.JSONField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default="")


# Table to store the embeddings of the users note
# add user later
# file_owner = models.ForeignKey(User, on_delete=models.CASCADE, default='')
