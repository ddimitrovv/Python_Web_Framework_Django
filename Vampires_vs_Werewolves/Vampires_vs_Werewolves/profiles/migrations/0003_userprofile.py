# Generated by Django 4.2.3 on 2023-07-16 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('hp', models.IntegerField(default=100)),
                ('mp', models.IntegerField(default=100)),
                ('level', models.IntegerField(default=1)),
                ('gold', models.IntegerField(default=100)),
            ],
        ),
    ]
