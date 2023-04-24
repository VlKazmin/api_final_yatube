from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Post."""

    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "text",
            "pub_date",
            "image",
            "group",
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Comment."""

    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "text", "created", "post")
        read_only_fields = ("post",)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow."""

    user = SlugRelatedField(
        slug_field="username",
        read_only=True
    )
    following = SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = (
            "user",
            "following",
        )

    def validate(self, data):
        user = self.context["request"].user
        following = data["following"]

        if user == following:
            raise serializers.ValidationError(
                "Вы не можете подписаться на самого себя"
            )
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого автора"
            )

        return data
