# Generated by Django 5.0.4 on 2024-04-11 15:11

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0005_alter_error_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='body',
            field=models.TextField(default=django.utils.timezone.now, verbose_name='Body'),
            preserve_default=False,
        ),
    ]
