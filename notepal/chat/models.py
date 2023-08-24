from django.db import models
import uuid
from django.contrib.auth.models import User
from pgvector.django import VectorField
from note.models import NoteFileembedding


class NoteEmbedding(models.Model):
    id = models.AutoField(primary_key=True)
    date_created = models.DateField(auto_now_add=True)
    file_text = models.TextField()
    file_embedding = models.ForeignKey(NoteFileembedding, on_delete=models.CASCADE)
    vector = VectorField(dimensions=384, null=True)


class History(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_question = models.TextField()
    llm_response = models.TextField()
    response_to_user = models.TextField()
    llm_algo_used = models.TextField()
    embedding_context = models.JSONField(null=True, blank=True)
