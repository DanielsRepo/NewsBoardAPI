from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["pk", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["pk", "post", "text", "creation_date", "author"]
        read_only_fields = ["creation_date", "author"]

    @staticmethod
    def get_author(obj):
        return obj.author.username


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "pk",
            "title",
            "author",
            "link",
            "creation_date",
            "upvotes_amount",
            "comments",
        ]
        read_only_fields = ["author", "link", "upvotes_amount", "creation_date"]

    @staticmethod
    def get_author(obj):
        return obj.author.username

    def get_comments(self, obj):
        queryset = Comment.objects.by_post(obj.pk)
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data
