from common.exceptions import (
    CannotLikeOwnPost,
    LikeAlreadyExists,
    LikeNotFound,
    PostNotFound,
)
from common.utils.custom_response_decorator import custom_response
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from posts.models import Post
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Like
from .response_schema import LIKE_ACTION_SCHEMA_RESPONSE


@custom_response
class PostLikeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses=LIKE_ACTION_SCHEMA_RESPONSE)
    def post(self, request, post_id):
        try:
            post = Post.objects.only("id", "author_id").get(id=post_id)
        except Post.DoesNotExist:
            raise PostNotFound

        if post.author_id == request.user.id:
            raise CannotLikeOwnPost

        try:
            Like.objects.create(user=request.user, post_id=post_id)
        except IntegrityError:
            raise LikeAlreadyExists

        return Response({"message": "Liked."}, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses=LIKE_ACTION_SCHEMA_RESPONSE)
    def delete(self, request, post_id):
        deleted, _ = Like.objects.filter(
            user=request.user, post_id=post_id
        ).delete()
        if not deleted:
            raise LikeNotFound
        return Response({"message": "Unliked."}, status=status.HTTP_200_OK)
