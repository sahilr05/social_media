from django.contrib import admin
from social_app.models import User

class UserAdmin(admin.ModelAdmin):
    ordering: list = ["-email"]
    list_display: list = [
        "user_id",
        "email",
        "username",
    ]


admin.site.register(User, UserAdmin)
