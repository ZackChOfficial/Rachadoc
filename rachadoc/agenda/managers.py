from django.db import models


class AgendaQuerySet(models.QuerySet):
    pass


class AgendaManager(models.Manager):
    def get_queryset(self):
        return AgendaQuerySet(self.model, using=self._db)
