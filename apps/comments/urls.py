from comments.views import (
    PostCommentDeleteAPIView,
    PostCommentListCreateAPIView,
)
from django.urls import path

urlpatterns = [
    path(
        "posts/<uuid:post_id>/comments/",
        PostCommentListCreateAPIView.as_view(),
        name="comments",
    ),
    path(
        "posts/<uuid:post_id>/comments/<uuid:pk>/",
        PostCommentDeleteAPIView.as_view(),
        name="comment-delete",
    ),
]
