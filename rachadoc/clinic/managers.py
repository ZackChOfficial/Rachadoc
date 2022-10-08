from django.db import models


class ClinicQuerySet(models.QuerySet):
    pass


class ClinicManager(models.Manager):
    def get_queryset(self):
        return ClinicQuerySet(self.model, using=self._db)
