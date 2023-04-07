from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUserModel


# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUserModel
    list_display = ("email", "name", "is_staff", "is_active")
    list_filter = ("email", "name", "is_staff", "is_active")
    ordering = ("email",)

    add_fieldsets = (
        (
            None,
            {
                "classes": "wide",
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "name", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions")},
        ),
    )


admin.site.register(CustomUserModel, CustomUserAdmin)
