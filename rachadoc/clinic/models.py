from django.db import models
from clinic.managers import ClinicManager
from django.utils.translation import gettext_lazy as _

from django.contrib.gis.db import models as gis_models
from core.lib.mixins import BaseTimestampedModel


class Clinic(BaseTimestampedModel):
    name = models.CharField(_("nom"), max_length=255)
    address = models.CharField(_("nom"), max_length=1024)
    point = gis_models.PointField()
    description = models.CharField(_("description"), max_length=4096)
    phone_number = models.CharField(_("numéro de téléphone"), max_length=255)
    email_address = models.CharField(_("adresse email"), max_length=255)
    objects = ClinicManager()
