from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.serializers import BaseModelSerializer
from .models import Post, Comment, Like


User = get_user_model()


class CommentSerializer(BaseModelSerializer):

    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all(),
        source="post"
    )

    class Meta:
        model = Comment
        fields = ("id", "author", "body")


class PostSerializer(BaseModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="author"
    )

    #TODO serializer author
    #перевикористати user serializers, зробити як read only поле тільки для відображення

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "author_id", "slug", "title", "body", "comments")

    #def validate(self, attrs):
    #    attrs["author"]
