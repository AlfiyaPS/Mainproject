# Generated by Django 4.2.5 on 2024-02-09 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0049_delete_location_remove_guide_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
