from django import forms

from inbox.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = (
            "display_name",
            "body",
            "requested_visibility",
        )
        error_messages = {  # noqa: RUF012
            "display_name": {"required": "Please enter your name."},
            "body": {"required": "Please enter a message."},
        }
