# Generated by Django 5.0.6 on 2024-06-12 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_remove_all_match_player1_remove_all_match_player2'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='unigue_id',
            field=models.CharField(default='0', max_length=100),
        ),
    ]