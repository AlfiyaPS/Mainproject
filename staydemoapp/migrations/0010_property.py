# Generated by Django 4.2.5 on 2023-10-24 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0009_remove_customuser_is_guest_remove_customuser_is_host_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('property_id', models.AutoField(primary_key=True, serialize=False)),
                ('property_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('property_type', models.CharField(max_length=100)),
                ('number_of_bedrooms', models.PositiveIntegerField()),
                ('number_of_bathrooms', models.PositiveIntegerField()),
                ('capacity', models.PositiveIntegerField()),
                ('availability_calendar', models.TextField()),
                ('images', models.ImageField(blank=True, null=True, upload_to='property_images/')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staydemoapp.host')),
            ],
        ),
    ]
