# Generated by Django 4.1.2 on 2022-11-24 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_url'),
        ('accounts', '0002_remove_myuser_city_remove_myuser_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraping.city'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraping.language'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='send_email',
            field=models.BooleanField(default=True),
        ),
    ]