from django.contrib import admin
from social_app.models import User, Follow

class UserAdmin(admin.ModelAdmin):
    ordering: list = ["-email"]
    list_display: list = [
        "user_id",
        "email",
        "username",
    ]


admin.site.register(User, UserAdmin)

class FollowAdmin(admin.ModelAdmin):
    list_display: list = [
        "follow_id",
        "user",
        "follower",
        "created_datetime",
        "deleted_datetime",
    ]

admin.site.register(Follow, FollowAdmin)