# Generated by Django 4.2.5 on 2023-11-02 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0018_delete_propertyapproval'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='approved',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
