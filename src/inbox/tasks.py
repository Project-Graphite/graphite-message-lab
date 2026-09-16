from celery import shared_task
from django.utils import timezone

from inbox.models import Message


@shared_task(ignore_result=True)
def process_message(message_id):
    message = Message.objects.get(pk=message_id)
    message.word_count = len(message.body.split())
    message.status = Message.Status.PROCESSED
    message.processed_at = timezone.now()
    message.save(update_fields=["word_count", "status", "processed_at"])
