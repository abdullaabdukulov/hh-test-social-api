import logging
from datetime import timedelta

from common.utils.email_sender import send_email_token
from django.utils import timezone

from config.celery import app


@app.task(name="send_message")
def send_verification_email_task(email: str, token: str):
    try:
        send_email_token(email=email, token=token)
    except Exception as exc:
        logging.exception(f"Error when sending verification email: {exc}")
        raise


@app.task(name="cleanup_unverified_users")
def cleanup_unverified_users(hours=48):
    from django.contrib.auth import get_user_model

    from .models import EmailVerificationToken

    User = get_user_model()
    cutoff = timezone.now() - timedelta(hours=hours)

    user_ids = (
        EmailVerificationToken.objects.filter(
            used_at__isnull=True, expires_at__lt=cutoff
        )
        .values_list("user_id", flat=True)
        .distinct()
    )

    deleted, _ = User.objects.filter(
        id__in=user_ids, is_verified=False
    ).delete()
    return deleted
