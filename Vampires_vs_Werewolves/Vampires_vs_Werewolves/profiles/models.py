from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

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
    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

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
        max_length=10,
        blank=True,
        null=True,
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
        # self_health = self.health
        # opponent_health = opponent.health

        self_total_damage = 0
        opponent_total_damage = 0

        winner = None
        loser = None

        # Fight for 3 rounds
        for _ in range(3):
            # Recalculate damage for each round based on power, defense, and speed
            self_damage = \
                max(0, self.total_power - (opponent.total_defence // 2) + (self.total_speed // 5)) // 10
            opponent_damage = \
                max(0, opponent.total_power - (self.total_defence // 2) + (opponent.total_speed // 5)) // 10

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
            winner.gold += int(0.3 * loser.gold)  # Winner receives 30% of the loser's gold
            winner.xp += winner.level * 5  # Increase winner's HP
            self.level = get_level_from_hp(winner.xp)  # Set winner level
            loser.gold -= int(0.3 * loser.gold) if int(0.3 * loser.gold) >= 0 else 0
            winner.health = max(0, winner.health)
            loser.health = max(0, loser.health)
            winner.wins += 1  # Increment wins for the winner
            loser.losses += 1  # Increment losses for the loser

            # Save the updated hero and opponent
            winner.save()
            loser.save()

        return winner

    def save(self, *args, **kwargs):
        # Calculate hourly_wage based on hero's level
        self.hourly_wage = self.level * 10
        self.total_power = self.power + self.sword.damage if self.sword else self.power
        self.total_defence = self.defence + self.shield.defence if self.shield else self.defence
        self.total_speed += self.speed + self.boots.speed_bonus if self.boots else self.speed
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f'Username: {CustomUser.objects.get(id=self.pk).username}'
