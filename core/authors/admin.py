from django.contrib import admin

from core.authors import models


class AuthorCustomAdmin(admin.ModelAdmin):
    search_fields = ["name", "email"]
    show_full_result_count = True
    list_filter = ["name", "email"]
    list_display = ["name", "email"]


admin.site.register(models.Author, AuthorCustomAdmin)
