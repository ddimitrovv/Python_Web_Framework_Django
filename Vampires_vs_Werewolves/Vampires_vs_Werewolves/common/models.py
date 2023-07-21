from django.db import models


class Sword(models.Model):
    name = models.CharField(max_length=100)
    damage = models.PositiveIntegerField(default=20)
    required_level = models.PositiveIntegerField(default=1)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name


class Shield(models.Model):
    name = models.CharField(max_length=100)
    defense = models.PositiveIntegerField(default=20)
    required_level = models.PositiveIntegerField(default=1)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name


class Boots(models.Model):
    name = models.CharField(max_length=100)
    speed_bonus = models.PositiveIntegerField(default=20)
    required_level = models.PositiveIntegerField(default=1)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.name
