# Generated by Django 4.2.5 on 2024-02-13 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0062_addservice_remove_service_features_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addservice',
            name='service_id',
            field=models.CharField(editable=False, max_length=50, unique=True),
        ),
    ]
