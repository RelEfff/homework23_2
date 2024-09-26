from django.contrib import admin

from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "is_published", "view_counter")
    list_filter = ("is_published",)
    search_fields = ("title", "content")
