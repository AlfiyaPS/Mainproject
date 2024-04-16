# Generated by Django 4.2.5 on 2023-11-05 04:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0025_alter_property_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='host',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
