from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('more information', {'fields': ('phone', 'city', 'country', 'department', 'role', 'birth_date', 'salary')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('more information', {'fields': ('phone', 'city', 'country', 'department', 'role', 'birth_date', 'salary')}),
    )

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'role', 'department', 'salary')

    search_fields = ('email', 'first_name', 'last_name', 'department', 'role')

    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'role', 'department', 'country')

    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)