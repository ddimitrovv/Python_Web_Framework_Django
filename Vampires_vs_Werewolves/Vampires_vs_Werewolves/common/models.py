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
    next_available_hiding_time = models.DateTimeField(default=timezone.now)

    def can_hide(self):
        # Check if the user can hide their profile based on the next available hiding time
        return timezone.now() >= self.next_available_hiding_time

    def hide_profile(self):
        # Hide the profile and update the hidden_at and next_available_hiding_time fields
        if self.can_hide():
            now = timezone.now()
            self.hidden_at = now
            self.next_available_hiding_time = now + timezone.timedelta(hours=12)
            self.save()
            return True
        return False
