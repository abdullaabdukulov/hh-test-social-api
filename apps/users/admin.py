from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

User = get_user_model()


@admin.register(User)
class UserModelAdmin(DjangoUserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "full_name",
        "is_verified",
        "is_active",
        "created_at",
    )
    list_filter = ("is_verified", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "username", "full_name", "id")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        ("Status", {"fields": ("is_verified", "is_active")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "full_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
