from django.contrib import admin
from django.template.defaultfilters import floatformat
from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'hero_type', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username']
    search_help_text = 'Search for user by username'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'xp', 'formatted_health', 'level', 'gold', 'gender',
                    'power', 'defence', 'speed', 'wins', 'losses', 'sword',
                    'shield', 'boots', 'hourly_wage', 'is_working']

    search_fields = ['user__username']
    search_help_text = 'Search for user profile by username'

    def formatted_health(self, obj):
        return floatformat(obj.health, 2)
    formatted_health.short_description = 'Health'
