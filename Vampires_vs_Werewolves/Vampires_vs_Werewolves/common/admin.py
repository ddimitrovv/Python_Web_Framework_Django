from django.contrib import admin

from Vampires_vs_Werewolves.common.models import Sword, Shield, Boots


@admin.register(Sword)
class SwordAdmin(admin.ModelAdmin):
    ...


@admin.register(Shield)
class SwordAdmin(admin.ModelAdmin):
    ...


@admin.register(Boots)
class SwordAdmin(admin.ModelAdmin):
    ...

