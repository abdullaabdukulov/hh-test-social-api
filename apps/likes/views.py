from common.utils.custom_response_decorator import custom_response
from django.db import IntegrityError
from posts.models import Post
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Like


@custom_response
class PostLikeAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, post_id):
        try:
            post = Post.objects.only("id", "author_id").get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound("Post not found.")

        if post.author_id == request.user.id:
            raise ValidationError({"detail": "You cannot like your own post."})

        try:
            Like.objects.create(user=request.user, post_id=post_id)
        except IntegrityError:
            raise ValidationError({"detail": "You already liked this post."})

        return Response({"message": "Liked."}, status=status.HTTP_200_OK)

    def delete(self, request, post_id):
        deleted, _ = Like.objects.filter(
            user=request.user, post_id=post_id
        ).delete()
        if not deleted:
            raise NotFound("Like not found.")
        return Response({"message": "Unliked."}, status=status.HTTP_200_OK)
