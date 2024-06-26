# Generated by Django 4.2.5 on 2024-02-13 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0066_remove_addservice_features_delete_feature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='addservice',
            name='features',
            field=models.ManyToManyField(blank=True, to='staydemoapp.feature'),
        ),
    ]
