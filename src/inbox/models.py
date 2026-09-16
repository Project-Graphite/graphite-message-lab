from django.db import models


class Message(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        PROCESSED = "processed", "Processed"

    display_name = models.CharField(max_length=80)
    body = models.TextField(max_length=500)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.QUEUED,
    )
    word_count = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]  # noqa: RUF012

    def __str__(self):
        return f"{self.display_name}: {self.body[:40]}"
