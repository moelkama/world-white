# Generated by Django 5.0.6 on 2024-06-12 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_all_match_score1_all_match_score2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='all_match',
            name='player1',
        ),
        migrations.RemoveField(
            model_name='all_match',
            name='player2',
        ),
    ]