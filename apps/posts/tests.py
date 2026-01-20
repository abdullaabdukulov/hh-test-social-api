import pytest
from django.contrib.auth import get_user_model
from posts.models import Post
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

POSTS_URL = "/api/v1/posts/"
FEED_URL = "/api/v1/feed/"


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_with_posts(db):
    user = User.objects.create_user(
        email="u@test.com",
        username="u1",
        full_name="U One",
        password="StrongPass123!",
    )
    user.is_verified = True
    user.save(update_fields=["is_verified"])

    Post.objects.create(author=user, title="T1", content="C1")
    Post.objects.create(author=user, title="T2", content="C2")
    return user


@pytest.mark.django_db
def test_feed_public(api_client, user_with_posts):
    resp = api_client.get(FEED_URL)
    assert resp.status_code == 200

    body = resp.json()
    assert body["success"] is True
    assert "data" in body


@pytest.fixture
def verified_user(db):
    user = User.objects.create_user(
        email="author@test.com",
        username="author_user",
        full_name="Author User",
        password="StrongPass123!",
    )
    user.is_verified = True
    user.save()
    return user


@pytest.fixture
def other_verified_user(db):
    user = User.objects.create_user(
        email="other@test.com",
        username="other_user",
        full_name="Other User",
        password="StrongPass123!",
    )
    user.is_verified = True
    user.save(update_fields=["is_verified"])
    return user


@pytest.fixture
def auth_client(api_client, verified_user):
    refresh = RefreshToken.for_user(verified_user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
    )
    return api_client


@pytest.fixture
def post(db, verified_user):
    return Post.objects.create(author=verified_user, title="T1", content="C1")


@pytest.mark.django_db
def test_posts_list_public(api_client, post):
    resp = api_client.get(POSTS_URL)
    assert resp.status_code == 200

    body = resp.json()
    assert body["success"] is True
    assert (
        "results" in body["data"]
        or isinstance(body["data"], list)
        or "data" in body
    )


@pytest.mark.django_db
def test_create_post_requires_auth(api_client):
    resp = api_client.post(
        POSTS_URL, {"title": "Hi", "content": "Body"}, format="json"
    )
    assert resp.status_code in (401, 403)


def test_create_post_success(auth_client):
    resp = auth_client.post(
        POSTS_URL,
        {"title": "Hello", "content": "Body"},
        format="json",
    )
    assert resp.status_code in (200, 201), resp.json()

    body = resp.json()
    assert body["success"] is True
    assert body["data"]["title"] == "Hello"


@pytest.mark.django_db
def test_post_detail_public(api_client, post):
    resp = api_client.get(f"{POSTS_URL}{post.id}/")
    assert resp.status_code == 200

    body = resp.json()
    assert body["success"] is True
    assert body["data"]["id"] == str(post.id)


@pytest.mark.django_db
def test_post_update_requires_owner(api_client, other_verified_user, post):
    refresh = RefreshToken.for_user(other_verified_user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
    )

    resp = api_client.patch(
        f"{POSTS_URL}{post.id}/", {"title": "New"}, format="json"
    )
    assert resp.status_code in (403, 404)  # IsOwner bo'lsa 403


@pytest.mark.django_db
def test_post_delete_owner(auth_client, post):
    resp = auth_client.delete(f"{POSTS_URL}{post.id}/")
    assert resp.status_code in (200, 204)

    assert not Post.objects.filter(id=post.id).exists()
