from comments.serializers import CommentSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post

User = get_user_model()


class FeedPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "title", "content", "likes")

    def get_likes(self, obj):
        return [str(like.user_id) for like in obj.likes.all()]


class FeedUserSerializer(serializers.ModelSerializer):
    posts = FeedPostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("username", "posts")


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "likes_count",
            "created_at",
            "updated_at",
        )


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content")


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "content",
            "likes",
            "comments",
            "created_at",
            "updated_at",
        )

    def get_likes(self, obj):
        return [str(like.user_id) for like in obj.likes.all()]
