from django.contrib import admin

from Vampires_vs_Werewolves.common.models import (Sword, Shield, Boots, Work,
                                                  PowerPotion, DefencePotion, SpeedPotion, HealthPotion)


@admin.register(Sword)
class SwordAdmin(admin.ModelAdmin):
    list_display = ['name', 'damage', 'required_level', 'price', 'sell_price']
    search_fields = ['name']
    search_help_text = 'Search for sword by sword name'


@admin.register(Shield)
class ShieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'defence', 'required_level', 'price', 'sell_price']
    search_fields = ['name']
    search_help_text = 'Search for shield by shield name'


@admin.register(Boots)
class BootsAdmin(admin.ModelAdmin):
    list_display = ['name', 'speed_bonus', 'required_level', 'price', 'sell_price']
    search_fields = ['name']
    search_help_text = 'Search for boots by boots name'


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'end_time', 'hours_worked', 'hourly_wage']
    search_fields = ['user']
    search_help_text = 'Search for work by username'


@admin.register(PowerPotion)
class PowerPotionAdmin(admin.ModelAdmin):
    list_display = ['type', 'price', 'hours_active', 'percent_bonus']


@admin.register(DefencePotion)
class DefencePotionAdmin(admin.ModelAdmin):
    list_display = ['type', 'price', 'hours_active', 'percent_bonus']


@admin.register(SpeedPotion)
class SpeedPotionAdmin(admin.ModelAdmin):
    list_display = ['type', 'price', 'hours_active', 'percent_bonus']


@admin.register(HealthPotion)
class HealthPotionAdmin(admin.ModelAdmin):
    list_display = ['type', 'price', 'hours_active', 'percent_bonus']
