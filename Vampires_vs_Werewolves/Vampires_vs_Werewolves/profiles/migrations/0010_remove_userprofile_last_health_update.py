# Generated by Django 4.2.3 on 2023-07-18 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_userprofile_last_health_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_health_update',
        ),
    ]
