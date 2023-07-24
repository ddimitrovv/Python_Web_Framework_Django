# Generated by Django 4.2.3 on 2023-07-22 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_boots_image_boots_required_level_shield_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='boots',
            name='price',
            field=models.PositiveIntegerField(default=70),
        ),
        migrations.AddField(
            model_name='shield',
            name='price',
            field=models.PositiveIntegerField(default=70),
        ),
        migrations.AddField(
            model_name='sword',
            name='price',
            field=models.PositiveIntegerField(default=70),
        ),
    ]