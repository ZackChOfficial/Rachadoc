from django.db import models
from django.utils.translation import gettext_lazy as _


class GENDERS(models.IntegerChoices):
    UNKNOWN = 1, _("Inconnu")
    MALE = 2, _("Homme")
    FEMALE = 3, _("Femme")


class CIVIL_STATUS(models.IntegerChoices):
    UNKNOWN = 1, _("Inconnu")
    MARRIED = 2, _("Marié")
    Single = 3, _("Célibataire")


class INSURANCES(models.IntegerChoices):
    UNKNOWN = 1, _("Inconnu")
