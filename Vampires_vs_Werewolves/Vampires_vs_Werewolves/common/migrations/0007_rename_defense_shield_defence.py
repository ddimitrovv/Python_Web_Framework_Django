# Generated by Django 4.2.3 on 2023-07-24 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_boots_sell_price_shield_sell_price_sword_sell_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shield',
            old_name='defense',
            new_name='defence',
        ),
    ]