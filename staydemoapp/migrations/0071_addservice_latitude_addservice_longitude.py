# Generated by Django 4.2.5 on 2024-02-20 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0070_addservice_guide'),
    ]

    operations = [
        migrations.AddField(
            model_name='addservice',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='addservice',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
