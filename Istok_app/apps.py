from django.apps import AppConfig


class IstokAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Istok_app'

    def ready(self):
        import Istok_app.signals