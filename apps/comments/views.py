from common.permissions import IsOwner, IsVerifiedOrReadOnly
from common.utils.custom_response_decorator import custom_response
from drf_yasg.utils import swagger_auto_schema
from posts.models import Post
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from .models import Comment
from .response_schema import (
    COMMENT_DELETE_SCHEMA_RESPONSE,
    COMMENTS_LIST_SCHEMA_RESPONSE,
)
from .serializers import CommentSerializer


@custom_response
class PostCommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsVerifiedOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return (
            Comment.objects.select_related("author")
            .filter(post_id=self.kwargs["post_id"])
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        post_id = self.kwargs["post_id"]
        if not Post.objects.filter(id=post_id).exists():
            raise NotFound("Post not found.")
        serializer.save(author=self.request.user, post_id=post_id)

    @swagger_auto_schema(responses=COMMENTS_LIST_SCHEMA_RESPONSE)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@custom_response
class PostCommentDeleteAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        if not post_id:
            return Comment.objects.none()
        return Comment.objects.filter(post_id=post_id)

    @swagger_auto_schema(responses=COMMENT_DELETE_SCHEMA_RESPONSE)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
