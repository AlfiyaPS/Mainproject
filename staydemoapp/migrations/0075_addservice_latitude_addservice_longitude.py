# Generated by Django 4.2.5 on 2024-02-20 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0074_remove_addservice_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='addservice',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='addservice',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
