# Generated by Django 4.2.3 on 2023-08-07 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_userhiding_potion_defencepotion_powerpotion_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='potion',
            name='user',
        ),
    ]
