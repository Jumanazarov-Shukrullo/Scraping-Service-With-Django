# Generated by Django 4.1.2 on 2022-11-27 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ('-timestamp',), 'verbose_name': 'Vacancy', 'verbose_name_plural': 'Vacancies'},
        ),
        migrations.AlterField(
            model_name='error',
            name='timestamp',
            field=models.DateField(auto_now_add=True),
        ),
    ]