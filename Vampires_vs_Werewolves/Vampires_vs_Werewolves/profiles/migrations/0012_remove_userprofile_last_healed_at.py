# Generated by Django 4.2.3 on 2023-07-21 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_userprofile_last_healed_at_userprofile_losses_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='last_healed_at',
        ),
    ]
