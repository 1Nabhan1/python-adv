# Generated by Django 5.2 on 2025-04-22 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0010_media_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='isAudio',
            field=models.BooleanField(default=True),
        ),
    ]
