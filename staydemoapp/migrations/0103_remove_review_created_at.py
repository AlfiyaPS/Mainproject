# Generated by Django 4.2.5 on 2024-03-16 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0102_alter_review_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='created_at',
        ),
    ]
