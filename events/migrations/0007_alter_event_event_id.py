# Generated by Django 5.0 on 2024-02-18 07:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
