from common.models import BaseModel
from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class Post(BaseModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        db_index=True,
    )
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(5)],
    )
    content = models.TextField(max_length=10_000)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title
