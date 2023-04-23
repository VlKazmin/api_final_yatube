from django.shortcuts import get_object_or_404

from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import LimitOffsetPagination


from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    GroupSerializer,
    PostSerializer,
    FollowSerializer,
)

from posts.models import Comment, Group, Post, Follow


class PostViewSet(viewsets.ModelViewSet):
    """
    Представление для просмотра, создания, редактирования и удаления постов.
    """

    queryset = Post.objects.select_related("author", "group")
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """
        Создает новый пост.
        """

        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для чтения групп. Доступно только чтение.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Представление для просмотра, создания, редактирования и удаления
    комментариев к постам.
    """

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]

    def get_queryset(self):
        """
        Возвращает queryset из всех комментариев к посту, идентификатор
        которого передается в параметрах запроса.
        """

        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        queryset = Comment.objects.select_related("author", "post").filter(
            post=post
        )
        return queryset

    def perform_create(self, serializer):
        """
        Создает новый комментарий и сохраняет его в базу данных.
        Автором комментария становится текущий пользователь.
        """

        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(author=self.request.user, post=post)

    def perform_update(self, serializer):
        """
        Обновляет данные существующего комментария в базе данных.
        Проверяет, что автором комментария является текущий пользователь.
        """

        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Изменение чужого комментария запрещено!")
        serializer.save()

    def perform_destroy(self, instance):
        """
        Удаляет существующий комментарий из базы данных.
        Проверяет, что автором комментария является текущий пользователь.
        """

        if instance.author != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужой комментарий")
        instance.delete()


class FollowViewSet(viewsets.ModelViewSet):
    """
    Представление для получения информации о конкретной подписке и
    создания новой подписки на автора.
    """

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter]
    search_fields = ["following__username"]

    def get_queryset(self):
        """
        Возвращает список подписок для текущего пользователя.
        """
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Создает новую подписку на автора.
        """
        following = serializer.validated_data["following"]
        if self.request.user == following:
            raise ValidationError("Вы не можете подписаться на самого себя")
        if self.get_queryset().filter(following=following).exists():
            raise ValidationError(f"Вы уже подписаны на {following}")
        serializer.save(user=self.request.user)
