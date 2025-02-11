# Generated by Django 5.1.5 on 2025-01-17 01:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library_app", "0002_alter_author_email_alter_reader_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookRequest",
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
                ("completed", models.BooleanField(default=False)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="requests",
                        to="library_app.book",
                    ),
                ),
                (
                    "reader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="requests",
                        to="library_app.reader",
                    ),
                ),
            ],
        ),
    ]
