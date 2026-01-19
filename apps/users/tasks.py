import logging

from common.utils.email_sender import send_email_token

from config.celery import app


@app.task(name="send_message")
def send_verification_email_task(email: str, token: str):
    try:
        send_email_token(email=email, token=token)
    except Exception as exc:
        logging.exception(f"Error when sending verification email: {exc}")
        raise
