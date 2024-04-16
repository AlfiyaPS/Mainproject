# Generated by Django 4.2.5 on 2024-02-28 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0084_delete_servicetimeslot'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('am_pm', models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='addservice',
            name='visit_times',
            field=models.ManyToManyField(blank=True, related_name='services', to='staydemoapp.visittime'),
        ),
    ]
