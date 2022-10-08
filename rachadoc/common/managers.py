from django.db import models


class TarifQuerySet(models.QuerySet):
    pass


class TarifManager(models.Manager):
    def get_queryset(self):
        return TarifQuerySet(self.model, using=self._db)


class PictureQuerySet(models.QuerySet):
    pass


class PictureManager(models.Manager):
    def get_queryset(self):
        return PictureQuerySet(self.model, using=self._db)


class ExpertiseQuerySet(models.QuerySet):
    pass


class ExpertiseManager(models.Manager):
    def get_queryset(self):
        return ExpertiseQuerySet(self.model, using=self._db)
