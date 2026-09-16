from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []  # noqa: RUF012

    operations = [  # noqa: RUF012
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("display_name", models.CharField(max_length=80)),
                ("body", models.TextField(max_length=500)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("queued", "Queued"),
                            ("processed", "Processed"),
                        ],
                        default="queued",
                        max_length=16,
                    ),
                ),
                (
                    "word_count",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("processed_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={"ordering": ["-created_at"]},
        )
    ]
