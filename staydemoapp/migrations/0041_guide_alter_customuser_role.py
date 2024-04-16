# Generated by Django 4.2.5 on 2024-02-06 00:00

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0040_remove_property_latitude_remove_property_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('is_guide', models.BooleanField(default=True)),
                ('is_host', models.BooleanField(default=False)),
                ('guide_first_name', models.CharField(max_length=30)),
                ('guide_last_name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('staydemoapp.customuser',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'guest'), (2, 'host'), (3, 'admin'), (4, 'guide')], default=1),
        ),
    ]