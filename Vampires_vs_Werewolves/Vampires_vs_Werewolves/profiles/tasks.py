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

        total_healing_time = 3 * 60  # 3 hours in minutes

        # Calculate the amount of health points to be added per minute
        healing_increment = max_health / total_healing_time

        while user_profile.health < max_health:
            time.sleep(60)
            user_profile.refresh_from_db()
            user_profile.health = min(user_profile.health + healing_increment, max_health)
            user_profile.save()

        # Healing is complete, set is_healing back to False
        user_profile.is_healing = False
        user_profile.save()

    return f"Healing for {user_profile} is complete."
