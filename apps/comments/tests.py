import pytest
from comments.models import Comment
from django.contrib.auth import get_user_model
from posts.models import Post
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def verified_user(db):
    user = User.objects.create_user(
        email="commenter@test.com",
        username="commenter",
        full_name="Commenter",
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
def test_comments_list_public(api_client, post):
    url = f"/api/v1/posts/{post.id}/comments/"
    resp = api_client.get(url)
    assert resp.status_code == 200

    body = resp.json()
    assert body["success"] is True


@pytest.mark.django_db
def test_create_comment_requires_auth(api_client, post):
    url = f"/api/v1/posts/{post.id}/comments/"
    resp = api_client.post(url, {"content": "Hi"}, format="json")
    assert resp.status_code in (401, 403)


@pytest.mark.django_db
def test_create_comment_success(auth_client, post):
    url = f"/api/v1/posts/{post.id}/comments/"
    resp = auth_client.post(url, {"content": "Hi"}, format="json")
    assert resp.status_code in (200, 201)

    assert Comment.objects.filter(post=post, content="Hi").exists()


@pytest.mark.django_db
def test_delete_comment_owner_only(auth_client, post, verified_user):
    c = Comment.objects.create(
        post=post, author=verified_user, content="To delete"
    )

    url = f"/api/v1/posts/{post.id}/comments/{c.id}/"
    resp = auth_client.delete(url)
    assert resp.status_code in (200, 204)

    assert not Comment.objects.filter(id=c.id).exists()
