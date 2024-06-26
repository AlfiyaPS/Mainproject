# Generated by Django 4.2.5 on 2024-02-28 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0090_delete_bookservice'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceBooking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_date', models.DateField()),
                ('number_of_guests', models.PositiveIntegerField()),
                ('additional_request', models.TextField(blank=True, null=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staydemoapp.guest')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staydemoapp.addservice')),
            ],
        ),
    ]
