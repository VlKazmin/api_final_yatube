from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение на редактирование и удаление только автору записи
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение для любых запросов
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем редактирование и удаление только автору записи
        return obj.author == request.user
