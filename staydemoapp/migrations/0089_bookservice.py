# Generated by Django 4.2.5 on 2024-02-28 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0088_addservice_capacity'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_name', models.CharField(max_length=255)),
                ('guest_email', models.EmailField(max_length=254)),
                ('booking_date', models.DateField()),
                ('number_of_guests', models.PositiveIntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('confirmed', models.BooleanField(default=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staydemoapp.addservice')),
            ],
        ),
    ]
