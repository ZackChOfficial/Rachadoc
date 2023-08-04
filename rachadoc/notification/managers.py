from django.db import models
from rachadoc.events.models import Appointement


class NotificationQuerySet(models.QuerySet):
    pass


class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def delete_by_appointement(self, appointement: Appointement, **kwargs):
        return self.filter(appointement__id=appointement.id, **kwargs).delete()
