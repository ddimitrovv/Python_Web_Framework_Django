from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.templatetags.tz import utc
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware

from Vampires_vs_Werewolves.common.models import Sword, Shield, Boots


def get_level_from_hp(hp, base_hp=100, multiplier=2.5):
    level = 1
    while hp >= base_hp:
        hp -= base_hp
        base_hp *= multiplier
        level += 1
    return level


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, is_staff=False, is_superuser=False):
        if not username:
            raise ValueError("The Username field must be set.")
        user = self.model(username=username, is_staff=is_staff, is_superuser=is_superuser)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class CustomUser(PermissionsMixin, AbstractBaseUser):

    class HeroTypes(models.TextChoices):
        Vampire = 'Vampire',
        Werewolf = 'Werewolf'

    username = models.CharField(
        max_length=150,
        unique=True,
    )

    email = models.EmailField(
        unique=True,
    )

    hero_type = models.CharField(
        choices=HeroTypes.choices,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    # Add the fields required for creating a user via the createsuperuser management command.
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    class Gender(models.TextChoices):
        FEMALE = 'Female', 'Female'
        MALE = 'Male', 'Male'

    xp = models.IntegerField(default=100)
    health = models.IntegerField(default=100)
    level = models.IntegerField(default=1)
    gold = models.IntegerField(default=100)
    gender = models.CharField(
        choices=Gender.choices,
        max_length=10
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    power = models.PositiveIntegerField(default=10)
    total_power = models.PositiveIntegerField(default=0)
    defence = models.PositiveIntegerField(default=10)
    total_defence = models.PositiveIntegerField(default=0)
    speed = models.PositiveIntegerField(default=10)
    total_speed = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    sword = models.ForeignKey(
        Sword,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    shield = models.ForeignKey(
        Shield,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    boots = models.ForeignKey(
        Boots,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    hourly_wage = models.PositiveIntegerField(default=10)
    is_working = models.BooleanField(default=False)

    def fight(self, opponent):
        self_health = self.health
        opponent_health = opponent.health

        self_total_damage = 0
        opponent_total_damage = 0

        winner = ''

        # Fight for 3 rounds
        for _ in range(3):
            # Recalculate damage for each round based on power, defense, and speed
            self_damage = max(0, self.total_power - (opponent.total_defence // 2) + (self.total_speed // 10))
            opponent_damage = max(0, opponent.total_power - (self.total_defence // 2) + (opponent.total_speed // 10))

            # Update total damage inflicted by each player
            self_total_damage += self_damage
            opponent_total_damage += opponent_damage

            # Reduce opponent's HP
            opponent_health -= self_damage

            # Check if opponent is defeated
            if opponent_health <= 0:
                break

            # Reduce self user's HP
            self_health -= opponent_damage

            # Check if self user is defeated
            if self_health <= 0:
                break

        # Determine the winner based on the total damage inflicted
        if self_total_damage > opponent_total_damage:
            self.gold += int(0.3 * opponent.gold)  # Winner receives 30% of the loser's gold
            self.xp += self.level * 5  # Increase winner's HP
            self.level = get_level_from_hp(self.xp)  # Set winner level
            opponent.gold -= int(0.3 * opponent.gold) if int(0.3 * opponent.gold) >= 0 else 0
            self.health -= opponent_total_damage if self.health - opponent_total_damage >= 0 else 0
            opponent.health -= self_total_damage if opponent.health - self_total_damage >= 0 else 0
            winner = self
            self.wins += 1  # Increment wins for the winner
            opponent.losses += 1  # Increment losses for the loser
        elif opponent_total_damage > self_total_damage:
            opponent.gold += int(0.3 * self.gold)  # Winner receives 30% of the loser's gold
            self.gold -= int(0.3 * self.gold) if int(0.3 * self.gold) >= 0 else 0
            opponent.xp += opponent.level  # Increase opponent HP
            opponent.level = get_level_from_hp(opponent.xp)  # Set opponent level
            opponent.health -= self_total_damage if opponent.health - self_total_damage >= 0 else 0
            self.health -= opponent_total_damage if self.health - opponent_total_damage >= 0 else 0
            winner = opponent
            opponent.wins += 1  # Increment wins for the winner
            self.losses += 1  # Increment losses for the loser

        # Save the updated hero and opponent
        self.save()
        opponent.save()
        return winner or None

    def save(self, *args, **kwargs):
        # Calculate hourly_wage based on hero's level
        self.hourly_wage = self.level * 10
        if self.sword:
            self.total_power = self.power + self.sword.damage
        if self.shield:
            self.total_defence = self.defence + self.shield.defence
        if self.sword:
            self.total_speed += self.speed + self.boots.speed_bonus
        super(UserProfile, self).save(*args, **kwargs)
