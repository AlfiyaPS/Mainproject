# Generated by Django 4.2.5 on 2024-02-13 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0063_alter_addservice_service_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='addservice',
            name='service_type',
            field=models.CharField(choices=[('adventurous', 'Adventurous'), ('picnic', 'Picnic'), ('cultural', 'Cultural'), ('music_concerts', 'Music/Concerts')], default='adventurous', max_length=20),
        ),
    ]