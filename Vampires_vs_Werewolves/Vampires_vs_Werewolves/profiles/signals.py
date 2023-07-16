from django.db.models.signals import post_save
from django.dispatch import receiver

from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(profile=instance)
