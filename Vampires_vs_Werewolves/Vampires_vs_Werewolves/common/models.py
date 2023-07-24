from django.db import models
from django.utils import timezone
from django.conf import settings


class Sword(models.Model):
    name = models.CharField(max_length=100)
    damage = models.PositiveIntegerField(default=20)
    required_level = models.PositiveIntegerField(default=1)
    image = models.ImageField(null=True)
    price = models.PositiveIntegerField(default=70)
    sell_price = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calculate sell price
        self.sell_price = int(self.price * 0.6)
        super(Sword, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Shield(models.Model):
    name = models.CharField(max_length=100)
    defence = models.PositiveIntegerField(default=20)
    required_level = models.PositiveIntegerField(default=1)
    image = models.ImageField(null=True)
    price = models.PositiveIntegerField(default=70)
    sell_price = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calculate sell price
        self.sell_price = int(self.price * 0.6)
        super(Shield, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Boots(models.Model):
    name = models.CharField(max_length=100)
    speed_bonus = models.PositiveIntegerField(default=20)
    required_level = models.PositiveIntegerField(default=1)
    image = models.ImageField(null=True)
    price = models.PositiveIntegerField(default=70)
    sell_price = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Calculate sell price
        self.sell_price = int(self.price * 0.6)
        super(Boots, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Work(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    hours_worked = models.PositiveIntegerField(default=0)
    hourly_wage = models.PositiveIntegerField(default=10)
