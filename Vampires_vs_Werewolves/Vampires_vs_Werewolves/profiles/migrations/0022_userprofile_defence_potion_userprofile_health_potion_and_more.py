# Generated by Django 4.2.3 on 2023-08-07 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0015_defencepotion_healthpotion_speedpotion'),
        ('profiles', '0021_userprofile_is_healing'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='defence_potion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.defencepotion'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='health_potion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.healthpotion'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='power_potion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.powerpotion'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='speed_potion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.speedpotion'),
        ),
    ]