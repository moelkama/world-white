# Generated by Django 5.0.6 on 2024-06-09 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserManagement', '0008_alter_userpro_photo_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpro',
            name='lose',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userpro',
            name='score',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='userpro',
            name='win',
            field=models.IntegerField(default=0),
        ),
    ]
