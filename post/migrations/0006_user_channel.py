# Generated by Django 3.1.4 on 2020-12-13 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20201212_0514'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='channel',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]