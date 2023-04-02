from django.db import models
from rachadoc.agendasetting.managers import AgendaSettingManager, ClinicAgendaSettingManager, DoctorAgendaSettingManager
from core.lib.mixins import BaseTimestampedModel
from django.utils.translation import gettext_lazy as _
from rachadoc.agendasetting.choices import WEEKDAYS
from rules.contrib.models import RulesModelMixin, RulesModelBase
import rules
from core.lib.permissions import is_doctor, is_doctor_and_same_clinic, is_doctor_and_AgendaSetting_owner


class AgendaSetting(BaseTimestampedModel):
    week_day = models.IntegerField(_("jour de semaine"), choices=WEEKDAYS.choices, default=WEEKDAYS.MONDAY)
    from_date = models.TimeField(_("heure de début"))
    to_date = models.TimeField(_("heure de fin"))
    objects = AgendaSettingManager()


class ClinicAgendaSetting(AgendaSetting, RulesModelMixin, metaclass=RulesModelBase):
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.CASCADE)
    objects = ClinicAgendaSettingManager()

    class Meta:
        rules_permissions = {
            "add": (rules.is_superuser | is_doctor_and_same_clinic),
            "change": (rules.is_superuser | is_doctor_and_same_clinic),
            "delete": (rules.is_superuser | is_doctor_and_same_clinic),
            "view": (rules.is_superuser | is_doctor_and_same_clinic),
            "list": (rules.is_superuser | is_doctor),
        }


class DoctorAgendaSetting(AgendaSetting, RulesModelMixin, metaclass=RulesModelBase):
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE)
    objects = DoctorAgendaSettingManager()

    class Meta:
        rules_permissions = {
            "add": (rules.is_superuser | is_doctor),
            "change": (rules.is_superuser | is_doctor_and_AgendaSetting_owner),
            "delete": (rules.is_superuser | is_doctor_and_AgendaSetting_owner),
            "view": (rules.is_superuser | is_doctor_and_AgendaSetting_owner),
            "list": (rules.is_superuser | is_doctor),
        }
