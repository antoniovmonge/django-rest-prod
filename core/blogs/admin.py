from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.core import paginator
from django.utils.functional import cached_property

from core.blogs import models


class BlogCustomAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    show_full_result_count = True
    list_filter = ["title"]
    list_display = ["title", "created_at"]
    date_hierarchy = "created_at"


admin.site.register(models.Blog, BlogCustomAdmin)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


# Idea referred from
# https://hakibenita.com/optimizing-the-django-admin-paginator
class CustomPaginator(paginator.Paginator):
    @cached_property
    def count(self):
        return 9999999
