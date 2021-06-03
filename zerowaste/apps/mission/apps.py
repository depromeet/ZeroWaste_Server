from django.apps import AppConfig


class MissionConfig(AppConfig):
    name = 'apps.mission'
    verbose_name = "Mission Application"

    def ready(self):
        import apps.mission.services.event_handlers
