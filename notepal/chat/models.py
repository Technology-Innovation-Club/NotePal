from django.db import models
import uuid
from django.contrib.auth.models import User


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
    metadata = models.JSONField(null=True, blank=True)
