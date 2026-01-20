import pytest
from django.contrib.auth import get_user_model
from likes.models import Like
from posts.models import Post
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def author(db):
    user = User.objects.create_user(
        email="author@test.com",
        username="author",
        full_name="Author",
        password="StrongPass123!",
    )
    user.is_verified = True
    user.save(update_fields=["is_verified"])
    return user


@pytest.fixture
def liker(db):
    user = User.objects.create_user(
        email="liker@test.com",
        username="liker",
        full_name="Liker",
        password="StrongPass123!",
    )
    user.is_verified = True
    user.save(update_fields=["is_verified"])
    return user


@pytest.fixture
def liker_client(api_client, liker):
    refresh = RefreshToken.for_user(liker)
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
    )
    return api_client


@pytest.fixture
def post(db, author):
    return Post.objects.create(author=author, title="T", content="C")


@pytest.mark.django_db
def test_like_requires_auth(api_client, post):
    url = f"/api/v1/posts/{post.id}/like/"
    resp = api_client.post(url)
    assert resp.status_code in (401, 403)


@pytest.mark.django_db
def test_cannot_like_own_post(api_client, author, post):
    refresh = RefreshToken.for_user(author)
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}"
    )

    url = f"/api/v1/posts/{post.id}/like/"
    resp = api_client.post(url)
    assert resp.status_code in (400, 403)

    body = resp.json()
    assert body["success"] is False


@pytest.mark.django_db
def test_like_success(liker_client, post, liker):
    url = f"/api/v1/posts/{post.id}/like/"
    resp = liker_client.post(url)
    assert resp.status_code == 200

    assert Like.objects.filter(user=liker, post=post).exists()


@pytest.mark.django_db
def test_like_twice_fails(liker_client, post, liker):
    Like.objects.create(user=liker, post=post)

    url = f"/api/v1/posts/{post.id}/like/"
    resp = liker_client.post(url)
    assert resp.status_code in (400, 409)

    body = resp.json()
    assert body["success"] is False


@pytest.mark.django_db
def test_unlike_success(liker_client, post, liker):
    Like.objects.create(user=liker, post=post)

    url = f"/api/v1/posts/{post.id}/like/"
    resp = liker_client.delete(url)
    assert resp.status_code == 200

    assert not Like.objects.filter(user=liker, post=post).exists()
