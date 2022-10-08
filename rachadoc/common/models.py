from django.db import models
from common.managers import TarifManager, PictureManager, ExpertiseManager
from clinic.models import Clinic
from django.utils.translation import gettext_lazy as _
from core.lib.mixins import BaseTimestampedModel


class Tarif(BaseTimestampedModel):
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    title = models.CharField(_("titre"), max_length=255)
    description = models.CharField(_("description"), max_length=4096)
    amount = models.FloatField(_("montant"))
    objects = TarifManager()


class Picture(BaseTimestampedModel):
    description = models.CharField(_("description"), max_length=1024)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    url = models.URLField()
    objects = PictureManager()


class Expertise(BaseTimestampedModel):
    name = models.CharField(_("nom"), max_length=255)
    description = models.CharField(_("description"), max_length=4096)
    objects = ExpertiseManager()
