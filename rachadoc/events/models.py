from django.db import models
from events.managers import EventManager, AppointementManager, PersonalManager
from core.lib.mixins import BaseTimestampedModel
from django.utils.translation import gettext_lazy as _
from events.choices import Status
from rules.contrib.models import RulesModelMixin, RulesModelBase
import rules
from core.lib.permissions import (
    is_doctor,
    is_event_owner,
    is_receptionist,
    is_doctor_and_same_clinic,
    is_receptionist_same_clinic,
)


class Event(BaseTimestampedModel, RulesModelMixin, metaclass=RulesModelBase):
    name = models.CharField(_("nom"), max_length=255)
    from_date = models.DateTimeField(_("date de début"))
    to_date = models.DateTimeField(_("date de fin"))
    status = models.IntegerField(_("Status"), choices=Status.choices, default=Status.UNKNOWN)
    objects = EventManager()


class Appointement(Event):
    patient = models.ForeignKey("accounts.Patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE)
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.CASCADE)
    note_pre_appointement = models.CharField(_("note pré rendez-vous "), max_length=2048)
    note_post_appointement = models.CharField(_("note après le rendez-vous"), max_length=2048)
    objects = AppointementManager()

    class Meta:
        rules_permissions = {
            "add": rules.is_superuser,
            "change": (rules.is_superuser | is_doctor_and_same_clinic | is_receptionist_same_clinic),
            "delete": rules.is_superuser,
            "view": (rules.is_superuser | is_doctor_and_same_clinic | is_receptionist_same_clinic),
            "list": (rules.is_superuser | is_doctor | is_receptionist),
        }


class Personal(Event):
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE)
    note = models.CharField(_("note"), max_length=2048)
    objects = PersonalManager()

    class Meta:
        rules_permissions = {
            "add": (rules.is_superuser | is_doctor),
            "change": (rules.is_superuser | is_event_owner),
            "delete": (rules.is_superuser | is_event_owner),
            "view": (rules.is_superuser | is_event_owner),
            "list": (rules.is_superuser | is_doctor),
        }
