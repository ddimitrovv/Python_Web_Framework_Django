import os

from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from Vampires_vs_Werewolves.common.models import Sword, Shield, Boots


@receiver(pre_delete, sender=Sword)
async def delete_file(sender, instance, **kwargs):
    if instance.image:
        path = os.path.join(settings.MEDIA_ROOT, instance.image.name)
        if os.path.isfile(path):
            os.remove(path)\



@receiver(pre_delete, sender=Shield)
async def delete_file(sender, instance, **kwargs):
    if instance.image:
        path = os.path.join(settings.MEDIA_ROOT, instance.image.name)
        if os.path.isfile(path):
            os.remove(path)


@receiver(pre_delete, sender=Boots)
def delete_file(sender, instance, **kwargs):
    if instance.image:
        path = os.path.join(settings.MEDIA_ROOT, instance.image.name)
        if os.path.isfile(path):
            os.remove(path)
