# Generated by Django 4.2.5 on 2024-02-13 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0065_feature_addservice_features'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addservice',
            name='features',
        ),
        migrations.DeleteModel(
            name='Feature',
        ),
    ]
