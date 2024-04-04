from django.shortcuts import get_object_or_404
from django.db import models

# Imports of CustomUser and UserProfile are inside the functions to break/avoid the circular dependency


def get_user_object(request):
    from Vampires_vs_Werewolves.profiles.models import CustomUser
    username = request.user
    return get_object_or_404(CustomUser, username=username)


def get_user_profile(request):
    from Vampires_vs_Werewolves.profiles.models import UserProfile
    user = get_user_object(request)
    return get_object_or_404(UserProfile, user=user)


def get_max_xp_for_current_level(hero):
    level = hero.level
    multiplier = 2.5
    base_xp = 250
    max_xp = base_xp * (multiplier ** (level - 1))
    return int(max_xp)


def get_max_health_for_current_level(hero):
    return int(get_health_from_level(hero.level))


def get_health_from_level(level):
    base_xp = 100
    multiplier = 2.5
    health = level * base_xp * multiplier
    return health


class HeroTypes(models.TextChoices):
    Vampire = 'Vampire',
    Werewolf = 'Werewolf'


class Gender(models.TextChoices):
    FEMALE = 'Female', 'Female'
    MALE = 'Male', 'Male'
