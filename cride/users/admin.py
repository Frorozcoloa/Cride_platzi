"""User models admin."""

#Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# models
from cride.users.models import User, Profile


class CustomUser(BaseUserAdmin):
    """User model admin."""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', "is_client")
    list_filter = ('is_client', 'is_staff', 'is_active', 'created', 'modified')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""
    list_display = ('user', 'reputation', 'rides_taken', 'rides_offered')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')


admin.site.register(User, CustomUser)