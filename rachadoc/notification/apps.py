from django.apps import AppConfig


class NotificationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rachadoc.notification"

    def ready(self):
        import notification.receivers  # noqa
