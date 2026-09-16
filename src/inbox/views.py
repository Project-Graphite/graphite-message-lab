import json
import logging

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from inbox.forms import MessageForm
from inbox.models import Message
from inbox.tasks import process_message

logger = logging.getLogger(__name__)


def serialize_message(message):
    return {
        "id": message.pk,
        "display_name": message.display_name,
        "body": message.body,
        "status": message.status,
        "word_count": message.word_count,
        "created_at": message.created_at.isoformat(),
    }


def enqueue_message(message_id):
    try:
        process_message.delay(message_id)
    except Exception:
        logger.exception("Could not enqueue message %s", message_id)


@require_http_methods(["GET", "POST"])
def messages(request):
    if request.method == "GET":
        recent = Message.objects.all()[:25]
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

    form = MessageForm(payload)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=422)

    with transaction.atomic():
        message = form.save()
        transaction.on_commit(lambda: enqueue_message(message.pk))

    return JsonResponse({"message": serialize_message(message)}, status=201)
