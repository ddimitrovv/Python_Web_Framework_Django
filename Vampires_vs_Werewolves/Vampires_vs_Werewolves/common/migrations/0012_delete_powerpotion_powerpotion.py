# Generated by Django 4.2.3 on 2023-08-07 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0011_remove_potion_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PowerPotion',
        ),
        migrations.CreateModel(
            name='PowerPotion',
            fields=[
                ('potion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.potion')),
            ],
            bases=('common.potion',),
        ),
    ]
