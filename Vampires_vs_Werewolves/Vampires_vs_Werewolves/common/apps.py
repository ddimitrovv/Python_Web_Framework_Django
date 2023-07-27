from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Vampires_vs_Werewolves.common'

    def ready(self):
        import Vampires_vs_Werewolves.common.signals
