from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройка раздела постов."""

    list_display = ("id", "text", "pub_date", "author", "group")
    list_editable = ("group",)
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"
    list_per_page = 15


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Настройка раздела групп."""

    list_display = ("description", "title", "slug", "id")
    list_editable = ("title", "slug",)
    search_fields = ("title",)
    list_filter = ("title",)
    empty_value_display = "-пусто-"
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Настройка раздела комментариев."""

    list_display = ("id", "post", "author", "text", "created")
    list_editable = ("author",)
    search_fields = ("text",)
    list_filter = ("author",)
    empty_value_display = "-пусто-"
    list_per_page = 10


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Класс настройки раздела подписок."""

    list_display = (
        'pk',
        'user',
        'following',
    )

    list_editable = ('following', "user",)
    list_filter = ('following',)
    list_per_page = 10
    search_fields = ('following',)
