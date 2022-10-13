from django.db import models


class AgendaSettingQuerySet(models.QuerySet):
    pass


class ClinicAgendaSettingQuerySet(AgendaSettingQuerySet):
    pass


class DoctorAgendaSettingQuerySet(AgendaSettingQuerySet):
    pass


class AgendaSettingManager(models.Manager):
    def get_queryset(self):
        return AgendaSettingQuerySet(self.model, using=self._db)


class ClinicAgendaSettingManager(models.Manager):
    def get_queryset(self):
        return ClinicAgendaSettingQuerySet(self.model, using=self._db)


class DoctorAgendaSettingManager(models.Manager):
    def get_queryset(self):
        return DoctorAgendaSettingQuerySet(self.model, using=self._db)
