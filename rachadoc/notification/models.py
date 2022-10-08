from django.db import models
from notification.managers import NotificationManager


class Notification(models.Model):
    objects = NotificationManager()
