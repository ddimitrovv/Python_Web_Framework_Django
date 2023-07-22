from django.contrib import admin

from Vampires_vs_Werewolves.profiles.models import CustomUser, UserProfile


@admin.register(CustomUser)
class SwordAdmin(admin.ModelAdmin):
    ...


@admin.register(UserProfile)
class SwordAdmin(admin.ModelAdmin):
    ...

