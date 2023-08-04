import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from celery import Celery

from Vampires_vs_Werewolves.profiles.models import UserProfile, get_max_health_for_current_level, CustomUser
from Vampires_vs_Werewolves.profiles.tasks import start_healing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Vampires_vs_Werewolves.settings')
settings.configure()

# Initialize Celery instance
app = Celery('Vampires_vs_Werewolves')
app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Load Django application
application = get_wsgi_application()


# Your logic to initiate automatic healing goes here
def initiate_automatic_healing(user_profile_ids):
    for user_profile_id in user_profile_ids:
        try:
            user_profile = UserProfile.objects.get(id=user_profile_id)
            max_health = get_max_health_for_current_level(user_profile)

            if user_profile.health < max_health:
                # If health is below max_health, start healing asynchronously
                start_healing.delay(user_profile.id)

        except UserProfile.DoesNotExist:
            print(f"UserProfile with ID {user_profile_id} not found.")
        except Exception as e:
            print(f"An error occurred while processing UserProfile with ID {user_profile_id}: {e}")


user_profile_ids = [user.pk for user in CustomUser.objects.all()]  # UserProfile ids
initiate_automatic_healing(user_profile_ids)

