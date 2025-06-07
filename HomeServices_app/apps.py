from django.apps import AppConfig


class HomeservicesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HomeServices_app'

    def ready(self):
        import HomeServices_app.signals  # Import signals when app is ready
