from django.contrib import admin

from inbox.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("display_name", "status", "word_count", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("display_name", "body")
    readonly_fields = ("status", "word_count", "processed_at", "created_at")
