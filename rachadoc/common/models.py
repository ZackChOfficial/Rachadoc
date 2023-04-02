from django.db import models
from rachadoc.common.managers import TarifManager, PictureManager, ExpertiseManager
from django.utils.translation import gettext_lazy as _
from core.lib.mixins import BaseTimestampedModel
from rules.contrib.models import RulesModelMixin, RulesModelBase
import rules
from core.lib.permissions import is_doctor, is_doctor_and_same_clinic, is_doctor_and_tarif_owner


class Tarif(BaseTimestampedModel, RulesModelMixin, metaclass=RulesModelBase):
    doctor = models.ForeignKey("accounts.Doctor", on_delete=models.CASCADE)
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.CASCADE)
    title = models.CharField(_("titre"), max_length=255)
    description = models.CharField(_("description"), max_length=4096)
    amount = models.FloatField(_("montant"))
    objects = TarifManager()

    class Meta:
        rules_permissions = {
            "add": rules.is_superuser,
            "change": (rules.is_superuser | is_doctor_and_tarif_owner),
            "delete": rules.always_deny,
            "view": (rules.is_superuser | is_doctor_and_tarif_owner),
            "list": rules.is_superuser,
        }


class Picture(BaseTimestampedModel, RulesModelMixin, metaclass=RulesModelBase):
    description = models.CharField(_("description"), max_length=1024)
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.CASCADE)
    url = models.URLField()
    objects = PictureManager()

    class Meta:
        rules_permissions = {
            "add": (rules.is_superuser | is_doctor),
            "change": (rules.is_superuser | is_doctor_and_same_clinic),
            "delete": rules.is_superuser,
            "view": (rules.always_allow),
            "list": rules.always_allow,
        }


class Expertise(BaseTimestampedModel, RulesModelMixin, metaclass=RulesModelBase):
    name = models.CharField(_("nom"), max_length=255)
    description = models.CharField(_("description"), max_length=4096)
    objects = ExpertiseManager()

    class Meta:
        rules_permissions = {
            "add": rules.is_superuser,
            "change": rules.is_superuser,
            "delete": rules.is_superuser,
            "view": rules.always_allow,
            "list": rules.always_allow,
        }
