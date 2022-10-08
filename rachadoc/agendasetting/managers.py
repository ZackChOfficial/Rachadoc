from django.db import models


class AgendaSettingQuerySet(models.QuerySet):
    pass


class AgendaSettingManager(models.Manager):
    def get_queryset(self):
        return AgendaSettingQuerySet(self.model, using=self._db)
