# Generated by Django 4.2.3 on 2023-07-21 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_remove_userprofile_last_health_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_healed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='losses',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wins',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
