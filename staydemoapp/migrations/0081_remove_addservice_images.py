# Generated by Django 4.2.5 on 2024-02-25 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0080_remove_addservice_images_addservice_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addservice',
            name='images',
        ),
    ]
