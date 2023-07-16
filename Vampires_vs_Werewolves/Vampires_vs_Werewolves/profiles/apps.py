from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Vampires_vs_Werewolves.profiles'

    def ready(self):
        import Vampires_vs_Werewolves.profiles.signals
        