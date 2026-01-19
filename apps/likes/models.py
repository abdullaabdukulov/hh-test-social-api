from common.models import BaseModel
from django.conf import settings
from django.db import models
from posts.models import Post


class Like(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
        db_index=True,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
        db_index=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="uniq_like_user_post",
            )
        ]

    def __str__(self):
        return f"{self.user} | {self.post}"
