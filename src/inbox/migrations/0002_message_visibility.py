from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = (("inbox", "0001_initial"),)

    operations = (
        migrations.AddField(
            model_name="message",
            name="is_public",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="message",
            name="moderation_flagged",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="message",
            name="requested_visibility",
            field=models.CharField(
                choices=[
                    ("private", "Private"),
                    ("public", "Public after review"),
                ],
                default="private",
                max_length=7,
            ),
        ),
    )
