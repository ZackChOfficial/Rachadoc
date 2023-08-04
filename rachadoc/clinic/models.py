from django.db import models
from rachadoc.clinic.managers import ClinicManager
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModelMixin, RulesModelBase
import rules

from django.contrib.gis.db import models as gis_models
from rachadoc.core.lib.mixins import BaseTimestampedModel
from rachadoc.core.lib.permissions import is_doctor_and_same_clinic
from auditlog.registry import auditlog


class Clinic(BaseTimestampedModel, RulesModelMixin, metaclass=RulesModelBase):
    name = models.CharField(_("nom"), max_length=255)
    address = models.CharField(_("addresse"), max_length=1024)
    point = gis_models.PointField()
    description = models.CharField(_("description"), max_length=4096)
    phone_number = models.CharField(_("numéro de téléphone"), max_length=255)
    email_address = models.CharField(_("adresse email"), max_length=255)
    objects = ClinicManager()

    class Meta:
        rules_permissions = {
            "add": rules.is_superuser,
            "change": (rules.is_superuser | is_doctor_and_same_clinic),
            "delete": rules.is_superuser,
            "view": (rules.is_superuser | is_doctor_and_same_clinic),
            "list": rules.is_superuser,
        }


auditlog.register(Clinic)
