from django.contrib import admin

from social_app.models import Comment
from social_app.models import Follow
from social_app.models import Post
from social_app.models import User


class UserAdmin(admin.ModelAdmin):
    ordering: list = ["-email"]
    list_display: list = [
        "user_id",
        "email",
        "username",
    ]


admin.site.register(User, UserAdmin)


class FollowAdmin(admin.ModelAdmin):
    ordering: list = ["-created_datetime"]
    list_display: list = [
        "follow_id",
        "user",
        "follower",
        "created_datetime",
        "deleted_datetime",
    ]


admin.site.register(Follow, FollowAdmin)


class PostAdmin(admin.ModelAdmin):
    ordering: list = ["-created_datetime"]
    list_display: list = [
        "post_id",
        "title",
        "description",
        "created_datetime",
        "deleted_datetime",
    ]


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    ordering: list = ["-created_datetime"]
    list_display: list = ["comment_id", "user", "post", "created_datetime"]


admin.site.register(Comment, CommentAdmin)
