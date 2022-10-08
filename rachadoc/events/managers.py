from django.db import models


class EventQuerySet(models.QuerySet):
    pass


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)


class AppointementQuerySet(models.QuerySet):
    pass


class AppointementManager(models.Manager):
    def get_queryset(self):
        return AppointementQuerySet(self.model, using=self._db)


class PersonalQuerySet(models.QuerySet):
    pass


class PersonalManager(models.Manager):
    def get_queryset(self):
        return PersonalQuerySet(self.model, using=self._db)
