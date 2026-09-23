import json

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from inbox.forms import MessageForm
from inbox.models import Message
from inbox.moderation import contains_flagged_language
from inbox.tasks import process_message


def serialize_message(message):
    return {
        "id": message.pk,
        "display_name": message.display_name,
        "body": message.body,
        "status": message.status,
        "word_count": message.word_count,
        "visibility": "public" if message.is_public else "private",
        "publication_requested": (
            message.requested_visibility == Message.Visibility.PUBLIC
        ),
        "moderation_flagged": message.moderation_flagged,
        "created_at": message.created_at.isoformat(),
    }


@require_http_methods(["GET", "POST"])
def messages(request):
    if request.method == "GET":
        recent = Message.objects.filter(
            is_public=True,
            requested_visibility=Message.Visibility.PUBLIC,
        )[:25]
        return JsonResponse(
            {"messages": [serialize_message(message) for message in recent]}
        )

    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        errors = {"body": ["Invalid JSON."]}
        return JsonResponse({"errors": errors}, status=400)
    if not isinstance(payload, dict):
        errors = {"body": ["Expected an object."]}
        return JsonResponse({"errors": errors}, status=400)
    payload.setdefault(
        "requested_visibility",
        Message.Visibility.PRIVATE,
    )

    form = MessageForm(payload)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=422)

    with transaction.atomic():
        message = form.save(commit=False)
        message.moderation_flagged = contains_flagged_language(
            f"{message.display_name} {message.body}"
        )
        if message.moderation_flagged:
            message.requested_visibility = Message.Visibility.PRIVATE
        message.save()
        transaction.on_commit(
            lambda: process_message.delay(message.pk), robust=True
        )

    return JsonResponse({"message": serialize_message(message)}, status=201)
