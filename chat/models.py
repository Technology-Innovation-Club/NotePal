from django.db import models
import uuid
from django.contrib.auth.models import User
from pgvector.django import VectorField
from note.models import NoteFileembedding


# Storing the user note chunks
class NoteEmbedding(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateField(auto_now_add=True)
    file_text = models.TextField()
    file_embedding = models.ForeignKey(NoteFileembedding, on_delete=models.CASCADE)
    vector = VectorField(dimensions=768, null=True)

# Storing the users chat history
class History(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    user_question = models.TextField(null=True, blank=True)
    llm_response = models.TextField(null=True, blank=True)
    response_to_user = models.TextField(null=True, blank=True)
    llm_algo_used = models.TextField(null=True, blank=True)
    embedding_context = models.JSONField(null=True, blank=True)
    file_uploaded = models.ForeignKey(
        NoteFileembedding, on_delete=models.CASCADE, null=True, blank=True
    )
    the_file = models.BinaryField(null=True, blank=True)
