"""
IEEE Standards App Configuration
"""
from django.apps import AppConfig

class IEEEStandardsConfig(AppConfig):
    """
    Configuration for IEEE Standards implementation
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ieee_standards'
    verbose_name = 'IEEE Standards Implementation'

    def ready(self):
        """
        Perform initialization when the app is ready
        """
        try:
            # Import signals if any
            import ieee_standards.signals  # noqa
        except ImportError:
            pass 