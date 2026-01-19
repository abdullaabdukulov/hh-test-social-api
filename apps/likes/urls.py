from django.urls import path
from likes.views import PostLikeAPIView

urlpatterns = [
    path(
        "posts/<uuid:post_id>/like/",
        PostLikeAPIView.as_view(),
        name="post-like",
    ),
]
