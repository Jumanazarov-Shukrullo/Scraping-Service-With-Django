# Generated by Django 4.1.2 on 2022-11-27 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0004_alter_vacancy_options_alter_error_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='error',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
