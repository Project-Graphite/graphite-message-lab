from django import forms

from inbox.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["display_name", "body"]  # noqa: RUF012

    def clean_display_name(self):
        value = self.cleaned_data["display_name"].strip()
        if not value:
            raise forms.ValidationError("Please enter your name.")
        return value

    def clean_body(self):
        value = self.cleaned_data["body"].strip()
        if not value:
            raise forms.ValidationError("Please enter a message.")
        return value
