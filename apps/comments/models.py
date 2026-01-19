from common.models import BaseModel
from django.conf import settings
from django.db import models
from posts.models import Post


class Comment(BaseModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True,
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        db_index=True,
    )

    content = models.TextField(max_length=2_000)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.post} | {self.author}"
