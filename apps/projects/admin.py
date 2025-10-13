from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from .models import Project, Task, UserTask


@admin.action(description="Mark selected items as deleted")
def make_deleted(modeladmin, request, queryset):
    for item in queryset:
        item.delete()


@admin.action(description="Restore selected items")
def make_restored(modeladmin, request, queryset):
    for item in queryset:
        item.restore()


class SoftDeletableAdmin(admin.ModelAdmin):
    actions = [make_deleted, make_restored]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        # Show all items (including soft-deleted) in admin by default.
        return self.model.objects.get_queryset()


@admin.register(Project)
class ProjectAdmin(SoftDeletableAdmin):
    list_display = ('name', 'author', 'created_at', 'is_deleted')
    list_filter = ('author', 'created_at', 'deleted_at')
    search_fields = ('name', 'author__username')
    ordering = ('-created_at',)
    filter_horizontal = ('users',)


@admin.register(Task)
class TaskAdmin(SoftDeletableAdmin):
    list_display = ('name', 'project', 'status', 'created_at', 'is_deleted')
    list_filter = ('project', 'status', 'created_at', 'deleted_at')
    search_fields = ('name', 'project__name')
    ordering = ('-created_at',)
    filter_horizontal = ('assignees',)


@admin.register(UserTask)
class UserTaskAdmin(SoftDeletableAdmin):
    list_display = ('user', 'task', 'created_at', 'is_deleted')
    list_filter = ('user', 'task__project', 'deleted_at')
    search_fields = ('user__username', 'task__name')
    ordering = ('-created_at',)