# Generated by Django 5.0.6 on 2024-06-12 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_all_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_match',
            name='score1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='all_match',
            name='score2',
            field=models.IntegerField(default=0),
        ),
    ]