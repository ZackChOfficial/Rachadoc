from django.db import models


class NotificationQuerySet(models.QuerySet):
    pass


class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)
