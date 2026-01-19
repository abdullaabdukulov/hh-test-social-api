from django.urls import path
from posts.views import (
    FeedAPIView,
    PostListCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("posts/", PostListCreateAPIView.as_view(), name="list-create"),
    path(
        "posts/<uuid:pk>/",
        PostRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
    path("feed/", FeedAPIView.as_view(), name="feed"),
]
