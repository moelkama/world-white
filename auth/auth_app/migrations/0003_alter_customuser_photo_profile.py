# Generated by Django 5.0.7 on 2024-07-11 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_remove_customuser_country_remove_customuser_timezone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo_profile',
            field=models.ImageField(default='default/avatar.svg', upload_to='User_profile'),
        ),
    ]
