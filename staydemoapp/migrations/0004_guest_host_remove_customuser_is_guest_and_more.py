# Generated by Django 4.2.5 on 2023-10-07 05:12

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('staydemoapp', '0003_customuser_property_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25, verbose_name='FISRT_NAME')),
                ('last_name', models.CharField(max_length=25, verbose_name='LAST_NAME')),
                ('phonenumber', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(max_length=254, verbose_name='E_MAIL')),
                ('username', models.CharField(max_length=25, unique=True, verbose_name='USERNAME')),
                ('password', models.CharField(max_length=25, verbose_name='PASSWORD')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('first_name', models.CharField(max_length=25, verbose_name='FISRT_NAME')),
                ('last_name', models.CharField(max_length=25, verbose_name='LAST_NAME')),
                ('property_name', models.CharField(max_length=25, verbose_name='PROPERTY_NAME')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('email', models.EmailField(max_length=254, verbose_name='E_MAIL')),
                ('username', models.CharField(max_length=25, unique=True, verbose_name='USERNAME')),
                ('password', models.CharField(max_length=25, verbose_name='PASSWORD')),
            ],
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_guest',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_host',
        ),
        migrations.AddField(
            model_name='customuser',
            name='license_upload',
            field=models.ImageField(blank=True, null=True, upload_to='licenses/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Guest'), (2, 'Host')], default=1),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='property_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
