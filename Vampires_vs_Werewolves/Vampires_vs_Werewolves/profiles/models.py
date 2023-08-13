from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.core.validators import MinValueValidator

from Vampires_vs_Werewolves.common.models import (Sword, Shield, Boots,
                                                  HealthPotion, PowerPotion, DefencePotion, SpeedPotion)


def get_level_from_hp(hp, base_hp=250, multiplier=2.5):
    level = 1
    while hp >= base_hp:
        hp -= base_hp
        base_hp *= multiplier
        level += 1
    return level


def get_max_hp_for_current_level(hero):
    level = hero.level
    max_hp = 0
    multiplier = 2.5
    base_hp = 250
    counter = 1
    while counter <= level:
        max_hp = base_hp * multiplier
        base_hp = max_hp
        counter += 1
    if level == 1:
        max_hp = base_hp
    return int(max_hp)


def get_max_health_for_current_level(hero):
    return int(get_health_from_level(hero.level))


def get_health_from_level(level, base_hp=100, multiplier=2.5):
    health = level * base_hp * multiplier
    return health


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


class HeroTypes(models.TextChoices):
    Vampire = 'Vampire',
    Werewolf = 'Werewolf'


class CustomUser(PermissionsMixin, AbstractBaseUser):
    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

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


class Gender(models.TextChoices):
    FEMALE = 'Female', 'Female'
    MALE = 'Male', 'Male'


class UserProfile(models.Model):

    xp = models.IntegerField(default=0)
    health = models.FloatField(
        default=250,
        validators=(
            MinValueValidator(0),
        ),
    )
    max_health_for_level = models.IntegerField(default=0)
    max_xp_for_level = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    gold = models.IntegerField(default=100)
    gender = models.CharField(
        choices=Gender.choices,
        max_length=10,
        blank=True,
        null=True,
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    power = models.PositiveIntegerField(default=10)
    power_bonus = models.PositiveIntegerField(default=0)
    total_power = models.PositiveIntegerField(default=0)
    defence = models.PositiveIntegerField(default=10)
    defence_bonus = models.PositiveIntegerField(default=0)
    total_defence = models.PositiveIntegerField(default=0)
    speed = models.PositiveIntegerField(default=10)
    speed_bonus = models.PositiveIntegerField(default=0)
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
    health_potion = models.ForeignKey(
        HealthPotion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    power_potion = models.ForeignKey(
        PowerPotion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    defence_potion = models.ForeignKey(
        DefencePotion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    speed_potion = models.ForeignKey(
        SpeedPotion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    hourly_wage = models.PositiveIntegerField(default=10)
    is_working = models.BooleanField(default=False)
    is_healing = models.BooleanField(default=False)
    is_hiding = models.BooleanField(default=False)

    def fight(self, opponent):
        min_damage = 3

        self_total_damage = 0
        opponent_total_damage = 0

        winner = None
        loser = None

        # Calculate the damage for each round based on power, defense, and speed
        self_damage = \
            max(min_damage, (self.total_power - (opponent.total_defence // 2) + (self.total_speed // 5)) // 2)
        opponent_damage = \
            max(min_damage, (opponent.total_power - (self.total_defence // 2) + (opponent.total_speed // 5)) // 2)

        # Fight for 3 rounds
        for _ in range(3):

            # Update total damage inflicted by each player
            self_total_damage += self_damage
            opponent_total_damage += opponent_damage

            # Reduce opponent's HP
            opponent.health -= self_damage

            # Check if opponent is defeated
            if opponent.health <= 0:
                winner = self
                loser = opponent
                break

            # Reduce self user's HP
            self.health -= opponent_damage

            # Check if self user is defeated
            if self.health <= 0:
                winner = opponent
                loser = self
                break

        if not winner and not loser:
            winner = self if self_total_damage > opponent_total_damage else opponent
            loser = self if self_total_damage < opponent_total_damage else opponent

        if winner and loser:
            current_winner_level = winner.level
            winner.gold += int(0.3 * loser.gold)  # Winner receives 30% of the loser's gold
            winner.xp += winner.level * 5  # Increase winner's HP
            winner.level = get_level_from_hp(winner.xp)  # Set winner level
            if winner.level > current_winner_level:
                winner.health = get_max_health_for_current_level(winner)
            loser.gold -= int(0.3 * loser.gold) if int(0.3 * loser.gold) >= 0 else 0
            winner.health = max(0.0, winner.health)
            loser.health = max(0.0, loser.health)
            winner.wins += 1  # Increment wins for the winner
            loser.losses += 1  # Increment losses for the loser

            # Save the updated hero and opponent
            winner.save()
            loser.save()

        return winner

    def save(self, *args, **kwargs):
        # Calculate hourly_wage based on hero's level
        self.hourly_wage = self.level * 10
        # Calculate total_power
        sword_power = self.sword.damage if self.sword else 0
        self.total_power = self.power + sword_power + self.power_bonus
        # Calculate total_defence
        shield_defence = self.shield.defence if self.shield else 0
        self.total_defence = self.defence + shield_defence + self.defence_bonus
        # Calculate total_speed
        boots_speed = self.boots.speed_bonus if self.boots else 0
        self.total_speed = self.speed + boots_speed + self.speed_bonus
        # Get max_health
        self.max_health_for_level = get_max_health_for_current_level(self)
        # Get max_xp
        self.max_xp_for_level = get_max_hp_for_current_level(self)

        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f'Username: {CustomUser.objects.get(id=self.pk)}'
