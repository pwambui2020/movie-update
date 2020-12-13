# Generated by Django 3.1.4 on 2020-12-13 15:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_user_channel'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='program',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]