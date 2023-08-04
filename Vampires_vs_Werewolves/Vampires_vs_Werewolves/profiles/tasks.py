import time
from celery import shared_task
from .models import get_max_health_for_current_level, UserProfile


@shared_task
def start_healing(user_profile_id):
    user_profile = UserProfile.objects.get(id=user_profile_id)
    max_health = get_max_health_for_current_level(user_profile)

    if not user_profile.is_healing:
        user_profile.is_healing = True
        user_profile.save()

        while user_profile.health < max_health:
            # Simulate some time for healing, adjust as needed
            time.sleep(10)
            user_profile.refresh_from_db()  # Refresh the user_profile from the database to get the latest value
            user_profile.health += 1
            user_profile.save()

        # Healing is complete, set is_healing back to False
        user_profile.is_healing = False
        user_profile.save()

    return f"Healing for {user_profile} is complete."
