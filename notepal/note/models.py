from django.db import models
import uuid
from pgvector.django import VectorField

# Create note file embedding model
class NoteFileembedding(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )
    name = models.TextField(unique=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    updated_ts = models.DateTimeField(auto_now=True)
    the_file = models.BinaryField()
    date_published = models.DateTimeField(null=True, blank=True)
    publisher = models.TextField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
 

class NoteEmbedding(models.Model):
    id = models.AutoField(primary_key=True)
    created_ts = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    file_embedding = models.ForeignKey(NoteFileembedding, on_delete=models.PROTECT)
    vector = VectorField(dimensions=1536, null=True)