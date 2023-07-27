from django.contrib import admin

from Vampires_vs_Werewolves.user_messages.models import CustomMessage


@admin.register(CustomMessage)
class CustomMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'content', 'timestamp']
