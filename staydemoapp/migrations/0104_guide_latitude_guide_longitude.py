# Generated by Django 4.2.5 on 2024-03-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0103_remove_review_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='guide',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
