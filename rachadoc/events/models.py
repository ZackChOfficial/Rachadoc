from django.db import models
from events.managers import EventManager, AppointementManager, PersonalManager
from core.lib.mixins import BaseTimestampedModel
from django.utils.translation import gettext_lazy as _
from events.choices import Status


class Event(BaseTimestampedModel):
    name = models.CharField(_("nom"), max_length=255)
    from_date = models.DateTimeField(_("date de début"))
    to_date = models.DateTimeField(_("date de fin"))
    status = models.IntegerField(_("Status"), choices=Status.choices, default=Status.UNKNOWN)
    object = EventManager()


class Appointement(Event):
    patient = models.ForeignKey("accounts.Patient", on_delete=models.CASCADE)
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE)
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.CASCADE)
    note_pre_appointement = models.CharField(_("note pré rendez-vous "), max_length=2048)
    note_post_appointement = models.CharField(_("note après le rendez-vous"), max_length=2048)
    objects = AppointementManager()


class PersonalEvent(Event):
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE)
    note = models.CharField(_("note"), max_length=2048)
    objects = PersonalManager()
