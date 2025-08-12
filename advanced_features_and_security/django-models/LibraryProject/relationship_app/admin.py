from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """Custom admin for CustomUser model"""

    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')

    # Fields to search by
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Filters in the right sidebar
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')

    # Add the custom fields to the form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

    # Fields to show when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

# Register the custom user with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
