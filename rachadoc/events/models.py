from django.db import models
from rachadoc.events.managers import EventManager, AppointementManager, PersonalManager
from rachadoc.core.lib.mixins import BaseTimestampedModel
from django.utils.translation import gettext_lazy as _
from rachadoc.events.choices import Status
from rules.contrib.models import RulesModelMixin, RulesModelBase
import rules
from rachadoc.core.lib.permissions import (
    is_doctor,
    is_event_owner,
    is_receptionist,
    is_doctor_and_same_clinic,
    is_receptionist_same_clinic,
)
import uuid


class Event(BaseTimestampedModel, RulesModelMixin, metaclass=RulesModelBase):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("nom"), max_length=255)
    start = models.DateTimeField(_("date de début"))
    end = models.DateTimeField(_("date de fin"))
    status = models.IntegerField(_("Status"), choices=Status.choices, default=Status.UNKNOWN)
    objects = EventManager()


class Appointement(Event):
    patient = models.ForeignKey("accounts.Patient", on_delete=models.PROTECT, related_name="_appointements")
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.PROTECT, related_name="_appointements")
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.PROTECT, related_name="_appointements")
    note_pre_appointement = models.CharField(_("note pré rendez-vous"), max_length=2048, blank=True, null=True)
    note_post_appointement = models.CharField(_("note après le rendez-vous"), max_length=2048, blank=True, null=True)
    waiting_examination = models.DateTimeField(_("Dans la salle d'attente"), default=None, blank=True, null=True)
    start_examination = models.DateTimeField(_("Début de l'examen"), default=None, blank=True, null=True)
    end_examination = models.DateTimeField(_("Fin de l'examen"), default=None, blank=True, null=True)
    send_sms = models.BooleanField(_("envoyer sms rappel"), default=False)
    send_email = models.BooleanField(_("envoyer email rappel"), default=False)
    creator = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, related_name="_creator", null=True)
    objects = AppointementManager()

    class Meta:
        rules_permissions = {
            "add": (is_doctor | is_receptionist),
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
