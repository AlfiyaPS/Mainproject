# Generated by Django 4.2.5 on 2024-02-25 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0079_serviceimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addservice',
            name='images',
        ),
        migrations.AddField(
            model_name='addservice',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='services', to='staydemoapp.serviceimage'),
        ),
    ]
