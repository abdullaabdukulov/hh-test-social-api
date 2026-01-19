from common.utils.custom_response_decorator import custom_response
from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from likes.models import Like
from rest_framework import generics, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.common.pagination import FeedPagination, PostPagination
from apps.common.permissions import IsOwner, IsVerifiedOrReadOnly

from .filters import PostFilter
from .models import Post
from .response_schema import (
    POST_DETAIL_SCHEMA_RESPONSE,
    POSTS_LIST_SCHEMA_RESPONSE,
)
from .serializers import (
    FeedUserSerializer,
    PostCreateUpdateSerializer,
    PostDetailSerializer,
    PostListSerializer,
)

User = get_user_model()


@custom_response
class FeedAPIView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = FeedUserSerializer
    pagination_class = FeedPagination

    def get_queryset(self):
        post_qs = (
            Post.objects.only("id", "author_id", "title", "content")
            .prefetch_related(
                Prefetch(
                    "likes", queryset=Like.objects.only("user_id", "post_id")
                )
            )
            .order_by("-created_at")
        )

        return (
            User.objects.only("id", "username")
            .prefetch_related(Prefetch("posts", queryset=post_qs))
            .order_by("username")
        )


@custom_response
class PostListCreateAPIView(generics.ListCreateAPIView):
    pagination_class = PostPagination
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = PostFilter
    search_fields = ("title", "content")
    ordering_fields = ("created_at", "likes_count")

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsVerifiedOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = Post.objects.select_related("author").order_by("-created_at")
        if self.request.method == "GET":
            qs = qs.annotate(likes_count=Count("likes"))
        return qs

    def get_serializer_class(self):
        return (
            PostCreateUpdateSerializer
            if self.request.method == "POST"
            else PostListSerializer
        )

    @swagger_auto_schema(responses=POSTS_LIST_SCHEMA_RESPONSE)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@custom_response
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]

        return [
            permissions.IsAuthenticated(),
            IsVerifiedOrReadOnly(),
            IsOwner(),
        ]

    def get_queryset(self):
        qs = Post.objects.select_related("author")

        if self.request.method == "GET":
            qs = qs.prefetch_related("comments__author", "likes__user")
        return qs

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    @swagger_auto_schema(responses=POST_DETAIL_SCHEMA_RESPONSE)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
