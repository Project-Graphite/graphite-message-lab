from django.contrib import admin

from inbox.models import Message


@admin.action(description="Publish selected messages")
def publish_messages(modeladmin, request, queryset):
    queryset.update(is_public=True)


@admin.action(description="Make selected messages private")
def make_messages_private(modeladmin, request, queryset):
    queryset.update(is_public=False)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "requested_visibility",
        "moderation_flagged",
        "is_public",
        "status",
        "created_at",
    )
    list_editable = ("is_public",)
    list_filter = (
        "is_public",
        "requested_visibility",
        "moderation_flagged",
        "status",
        "created_at",
    )
    search_fields = ("display_name", "body")
    readonly_fields = (
        "requested_visibility",
        "moderation_flagged",
        "status",
        "word_count",
        "processed_at",
        "created_at",
    )
    actions = (publish_messages, make_messages_private)


admin.site.site_header = "Graphite Message Lab"
admin.site.site_title = "Graphite Message Lab"
admin.site.index_title = "Private inbox"
