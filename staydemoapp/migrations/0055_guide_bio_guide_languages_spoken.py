# Generated by Django 4.2.5 on 2024-02-11 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0054_alter_guide_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='guide',
            name='languages_spoken',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
