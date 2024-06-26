# Generated by Django 4.2.5 on 2024-02-27 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0082_addservice_images_delete_serviceimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.TimeField()),
                ('capacity', models.PositiveIntegerField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staydemoapp.addservice')),
            ],
        ),
    ]
