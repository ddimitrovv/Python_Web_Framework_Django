# Generated by Django 4.2.3 on 2023-07-23 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_userprofile_boots_userprofile_shield_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='hourly_wage',
            field=models.PositiveIntegerField(default=10),
        ),
    ]
