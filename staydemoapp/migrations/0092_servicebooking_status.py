# Generated by Django 4.2.5 on 2024-03-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0091_servicebooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicebooking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
