from django.contrib import admin

from core.blogs import models


class BlogCustomAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    show_full_result_count = True
    list_filter = ["title"]
    list_display = ["title", "created_at"]
    date_hierarchy = "created_at"


admin.site.register(models.Blog, BlogCustomAdmin)
