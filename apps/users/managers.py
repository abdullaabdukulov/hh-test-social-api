from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from .tasks import send_verification_email_task


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError("Email must be set")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, **extra_fields)
        if not password:
            raise ValidationError("Password must be set")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)

    @transaction.atomic
    def register_user(self, *, email, username, full_name, password):
        from .models import EmailVerificationToken

        if not email:
            raise ValidationError("Email must be set.")
        if not password:
            raise ValidationError("Password must be set.")

        email = self.normalize_email(email).lower()
        user = self.model(
            email=email,
            username=username.strip(),
            full_name=full_name.strip(),
            is_verified=False,
            is_active=True,
        )
        user.set_password(password)

        try:
            user.save(using=self._db)
        except IntegrityError as exc:
            raise ValidationError(
                "User with this email/username already exists."
            ) from exc

        token_obj = EmailVerificationToken.issue_for(user, ttl_hours=24)
        self.send_verification_email(
            to_email=user.email, token=str(token_obj.token)
        )
        return user, token_obj

    def send_verification_email(self, *, to_email, token):
        send_verification_email_task.delay(email=to_email, token=token)
