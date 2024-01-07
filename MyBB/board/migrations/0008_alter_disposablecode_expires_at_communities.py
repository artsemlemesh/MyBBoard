# Generated by Django 4.2.3 on 2024-01-02 03:27

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("board", "0007_remove_comment_rate_alter_disposablecode_expires_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="disposablecode",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 2, 3, 28, 46, 402778, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.CreateModel(
            name="Communities",
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
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("members", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
