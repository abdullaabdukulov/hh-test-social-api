from comments.models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "content", "created_at")
