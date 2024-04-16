# Generated by Django 4.2.5 on 2024-02-13 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0060_service_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='duration_hours',
        ),
        migrations.AddField(
            model_name='service',
            name='duration_minutes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
