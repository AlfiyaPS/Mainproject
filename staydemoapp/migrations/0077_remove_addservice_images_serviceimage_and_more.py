# Generated by Django 4.2.5 on 2024-02-25 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0076_remove_addservice_latitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addservice',
            name='images',
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='service_images/')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_images', to='staydemoapp.addservice')),
            ],
        ),
        migrations.AddField(
            model_name='addservice',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='services', to='staydemoapp.serviceimage'),
        ),
    ]