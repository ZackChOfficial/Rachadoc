from django.db import models
from agendasetting.managers import AgendaSettingManager, ClinicAgendaSettingManager, DoctorAgendaSettingManager
from core.lib.mixins import BaseTimestampedModel
from django.utils.translation import gettext_lazy as _
from agendasetting.choices import WEEKDAYS


class AgendaSetting(BaseTimestampedModel):
    week_day = models.IntegerField(_("jour de semaine"), choices=WEEKDAYS.choices, default=WEEKDAYS.MONDAY)
    from_date = models.DateTimeField(_("date de début"))
    to_date = models.DateTimeField(_("date de fin"))
    objects = AgendaSettingManager()


class ClinicAgendaSetting(AgendaSetting):
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.CASCADE)
    objects = ClinicAgendaSettingManager()


class DoctorAgendaSetting(AgendaSetting):
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE)
    objects = DoctorAgendaSettingManager()
