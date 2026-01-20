import uuid
from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import EmailVerificationToken
from users.tasks import cleanup_unverified_users

User = get_user_model()

REGISTER_URL = "/api/v1/auth/register/"
LOGIN_URL = "/api/v1/auth/login/"
ME_URL = "/api/v1/auth/me/"
USER_ME_PATCH_URL = "/api/v1/users/me/"
VERIFY_EMAIL_URL = "/api/v1/auth/verify-email/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def verified_user(db):
    user = User.objects.create_user(
        email="verified@test.com",
        username="verified_user",
        full_name="Verified User",
        password="StrongPass123!",
    )
    user.is_verified = True
    user.save(update_fields=["is_verified"])
    return user


@pytest.fixture
def unverified_user(db):
    return User.objects.create_user(
        email="unverified@test.com",
        username="unverified_user",
        full_name="Unverified User",
        password="StrongPass123!",
    )


@pytest.fixture
def auth_client(api_client, verified_user):
    refresh = RefreshToken.for_user(verified_user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
    )
    return api_client


@pytest.mark.django_db
def test_register_creates_user_and_token(api_client):
    payload = {
        "email": "new@test.com",
        "username": "new_user",
        "full_name": "New User",
        "password": "StrongPass123!",
    }

    resp = api_client.post(REGISTER_URL, payload, format="json")
    assert resp.status_code in (200, 201)

    body = resp.json()
    assert body["success"] is True
    assert "data" in body
    assert body["data"]["email"] == payload["email"]
    assert body["data"]["username"] == payload["username"]
    assert body["data"]["full_name"] == payload["full_name"]
    assert "message" in body["data"]

    user = User.objects.get(email=payload["email"])
    assert user.is_verified is False
    assert user.check_password(payload["password"]) is True

    assert EmailVerificationToken.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_verify_email_marks_user_verified(api_client, unverified_user):
    token_obj = EmailVerificationToken.objects.create(
        user=unverified_user,
        token=uuid.uuid4(),
        expires_at=timezone.now() + timedelta(hours=24),
    )

    resp = api_client.get(f"{VERIFY_EMAIL_URL}?token={token_obj.token}")
    assert resp.status_code == 200

    body = resp.json()
    assert body["success"] is True

    unverified_user.refresh_from_db()
    assert unverified_user.is_verified is True

    token_obj.refresh_from_db()
    assert token_obj.used_at is not None


@pytest.mark.django_db
def test_login_returns_access_token(api_client, verified_user):
    payload = {"email": verified_user.email, "password": "StrongPass123!"}

    resp = api_client.post(LOGIN_URL, payload, format="json")
    assert resp.status_code == 200

    body = resp.json()
    assert body["success"] is True
    assert "access" in body["data"]


@pytest.mark.django_db
def test_me_requires_auth(api_client):
    resp = api_client.get(ME_URL)
    assert resp.status_code in (401, 403)

    body = resp.json()
    assert body["success"] is False
    assert body["errors"]


@pytest.mark.django_db
def test_me_returns_current_user(auth_client, verified_user):
    resp = auth_client.get(ME_URL)
    assert resp.status_code == 200

    body = resp.json()
    assert body["success"] is True
    assert body["data"]["email"] == verified_user.email
    assert body["data"]["username"] == verified_user.username


@pytest.mark.django_db
def test_patch_users_me_updates_profile(auth_client, verified_user):
    payload = {"full_name": "Updated Name", "username": "updated_username"}

    resp = auth_client.patch(USER_ME_PATCH_URL, payload, format="json")
    assert resp.status_code in (200, 202)

    verified_user.refresh_from_db()
    assert verified_user.full_name == payload["full_name"]
    assert verified_user.username == payload["username"]


@pytest.mark.django_db
def test_cleanup_unverified_users_deletes_old_unverified(db):
    user = User.objects.create_user(
        email="old_unverified@test.com",
        username="old_unverified",
        full_name="Old Unverified",
        password="StrongPass123!",
    )

    with freeze_time(timezone.now() - timedelta(hours=72)):
        EmailVerificationToken.objects.create(
            user=user,
            token=uuid.uuid4(),
            expires_at=timezone.now() - timedelta(hours=1),
        )

    deleted = cleanup_unverified_users(hours=48)
    assert deleted >= 1
    assert not User.objects.filter(email="old_unverified@test.com").exists()
