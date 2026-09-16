import json
from unittest.mock import patch

from django.test import TestCase

from inbox.models import Message
from inbox.tasks import process_message


class MessageApiTests(TestCase):
    def test_lists_messages(self):
        Message.objects.create(display_name="Ada", body="Hello Graphite")

        response = self.client.get("/api/messages/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["messages"][0]["display_name"], "Ada")

    @patch("inbox.views.process_message.delay")
    def test_creates_and_queues_message(self, delay):
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                "/api/messages/",
                data=json.dumps({"display_name": "Grace", "body": "Ship it"}),
                content_type="application/json",
            )

        self.assertEqual(response.status_code, 201)
        message = Message.objects.get()
        self.assertEqual(message.body, "Ship it")
        delay.assert_called_once_with(message.pk)

    def test_rejects_empty_message(self):
        response = self.client.post(
            "/api/messages/",
            data=json.dumps({"display_name": "", "body": ""}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(Message.objects.count(), 0)

    def test_rejects_non_object_json(self):
        response = self.client.post(
            "/api/messages/",
            data="[]",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)


class MessageTaskTests(TestCase):
    def test_processes_message(self):
        message = Message.objects.create(
            display_name="Linus",
            body="Talk is cheap show me the code",
        )

        process_message(message.pk)

        message.refresh_from_db()
        self.assertEqual(message.status, Message.Status.PROCESSED)
        self.assertEqual(message.word_count, 7)
        self.assertIsNotNone(message.processed_at)
