# Generated by Django 4.2.5 on 2023-10-02 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0002_customuser_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='property_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
