import time
from celery import shared_task
from datetime import datetime, timedelta
from .models import get_max_health_for_current_level, UserProfile
from ..common.models import Attack


@shared_task
def start_healing(user_profile_id):
    # Start healing process to user and stop when user health is the max for current level
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


@shared_task
def remove_bonus(user_profile_id, field_to_update):
    # Remove the potion bonus when the potion effect expired
    user_profile = UserProfile.objects.get(pk=user_profile_id)

    # Set profile bonus field to 0 when the potion expires
    setattr(user_profile, field_to_update, 0)
    user_profile.save()

    return f'Removed {field_to_update} for {user_profile}.'


# @shared_task
# def reset_attack_counts():
#     # Reset user attacks to other user every day
#     # Get the current date and time
#     now = datetime.now()
#     # Calculate the start of the next day
#     next_day_start = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
#     # Reset attack counts for all users
#     Attack.objects.all().update(attacks=0)
#     # Calculate the time difference in seconds
#     seconds_until_next_day = (next_day_start - now).total_seconds()
#     # Calculate remaining time in hours and minutes
#     hours_until_next_day = seconds_until_next_day // 3600
#     minutes_until_next_day = (seconds_until_next_day % 3600) // 60
#     # Schedule the task again for the next day
#     reset_attack_counts.apply_async(countdown=seconds_until_next_day)
#
#     return (f'All attack counters are reset successfully! Next reset in'
#             f' {hours_until_next_day:.0f} hours: {minutes_until_next_day:.0f} minutes')


@shared_task
def reset_attack_counts():
    # Reset attack counts for all users
    Attack.objects.all().update(attacks=0)

    return 'All attack counters are reset successfully!'
