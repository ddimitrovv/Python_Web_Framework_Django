# Generated by Django 4.2.3 on 2023-07-18 07:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_rename_hp_userprofile_health_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_health_update',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]