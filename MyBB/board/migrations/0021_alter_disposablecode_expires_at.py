# Generated by Django 5.0 on 2024-01-09 00:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("board", "0020_message_description_message_image_message_video_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="disposablecode",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 9, 0, 40, 44, 996864, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
