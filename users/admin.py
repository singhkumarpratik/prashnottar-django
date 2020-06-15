from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "slug",
    )
    fieldsets = UserAdmin.fieldsets + (("Bio", {"fields": ("bio",),}),)


@admin.register(models.Follow)
class CustomFollowAdmin(admin.ModelAdmin):
    pass
