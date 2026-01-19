import uuid
from datetime import timedelta

from common.models import BaseModel
from common.validators import username_validator
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=32, validators=[username_validator], unique=True
    )
    full_name = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    def __str__(self):
        return self.username


class EmailVerificationToken(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verification_tokens",
    )
    token = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["token"])]

    @classmethod
    def issue_for(cls, user, ttl_hours: int = 24):
        return cls.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(hours=ttl_hours),
        )

    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    def is_used(self) -> bool:
        return self.used_at is not None
