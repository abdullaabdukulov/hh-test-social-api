from django.conf import settings
from django.core.mail import send_mail


def send_email_token(*, email, token):
    verify_url = (
        f"{settings.PUBLIC_BASE_URL}{settings.EMAIL_VERIFY_PATH}?token={token}"
    )

    send_mail(
        subject="Verify your email",
        message=(
            "User created successfully.\n\n"
            "Please verify your email by opening this link:\n"
            f"{verify_url}\n"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
