from abc import abstractmethod
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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
    class Meta:
        verbose_name = 'Boots'
        verbose_name_plural = 'Boots'

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

    def __str__(self):
        return f'{self.__class__.__name__} - {self.user}'


class UserHiding(models.Model):
    user = models.OneToOneField('profiles.UserProfile', on_delete=models.CASCADE)
    hidden_at = models.DateTimeField(default=timezone.now)
    can_stop_hiding_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate when user can stop hiding (min hiding time = 12 hours)
        self.can_stop_hiding_at = self.hidden_at + timedelta(hours=12)
        super(UserHiding, self).save(*args, **kwargs)


class PotionTypes(models.TextChoices):
    Health = 'Health',
    Power = 'Power',
    Defence = 'Defence',
    Speed = 'Speed',


class Potion(models.Model):
    class Meta:
        abstract = True

    @property
    @abstractmethod
    def type(self):
        ...

    price = models.PositiveIntegerField(blank=True, null=True)
    hours_active = models.PositiveIntegerField(
        default=1,
        validators=(
            MinValueValidator(1),
            MaxValueValidator(24)
        ),
    )
    image = models.ImageField()
    percent_bonus = models.PositiveIntegerField(default=10)

    def save(self, *args, **kwargs):
        # Calculate the potion price
        self.price = self.percent_bonus * self.hours_active * 10
        super(Potion, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.type}'


class PowerPotion(Potion):
    @property
    def type(self):
        return PotionTypes.Power


class DefencePotion(Potion):
    @property
    def type(self):
        return PotionTypes.Defence


class SpeedPotion(Potion):
    @property
    def type(self):
        return PotionTypes.Speed


class HealthPotion(Potion):
    @property
    def type(self):
        return PotionTypes.Health

