from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "full_name",
        "is_active",
        "created_at",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "username", "full_name", "id")
    ordering = ("full_name",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "full_name",
                    "email",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser"),
            },
        ),
    )
