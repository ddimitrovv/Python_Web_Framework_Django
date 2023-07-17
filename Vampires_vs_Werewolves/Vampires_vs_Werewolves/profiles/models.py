from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


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
        Female = 'Female',
        Male = 'Male'

    hp = models.IntegerField(default=100)
    mp = models.IntegerField(default=100)
    level = models.IntegerField(default=1)
    gold = models.IntegerField(default=100)
    gender = models.CharField(
        choices=Gender.choices,
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
    )
    power = models.PositiveIntegerField(default=10)
    defence = models.PositiveIntegerField(default=10)
    speed = models.PositiveIntegerField(default=10)

    def fight(self, opponent):
        self_hp = self.hp
        opponent_hp = opponent.hp

        self_total_damage = 0
        opponent_total_damage = 0

        # Fight for 3 rounds
        for _ in range(3):
            # Recalculate damage for each round based on power, defense, and speed
            self_damage = max(0, self.power - (opponent.defence // 2) + (self.speed // 10))
            opponent_damage = max(0, opponent.power - (self.defence // 2) + (opponent.speed // 10))

            # Update total damage inflicted by each player
            self_total_damage += self_damage
            opponent_total_damage += opponent_damage

            # Reduce opponent's HP
            opponent_hp -= self_damage

            # Check if opponent is defeated
            if opponent_hp <= 0:
                break

            # Reduce self user's HP
            self_hp -= opponent_damage

            # Check if self user is defeated
            if self_hp <= 0:
                break

        # Determine the winner based on the total damage inflicted
        if self_total_damage > opponent_total_damage:
            self.gold += int(0.3 * opponent.gold)  # Winner receives 30% of the loser's gold
            opponent.gold -= int(0.3 * opponent.gold)
        elif opponent_total_damage > self_total_damage:
            opponent.gold += int(0.3 * self.gold)  # Winner receives 30% of the loser's gold

        # Save the updated hero and opponent
        self.save()
        opponent.save()
