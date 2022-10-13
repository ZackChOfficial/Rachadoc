from calendar import FRIDAY, SATURDAY, SUNDAY, THURSDAY, TUESDAY, WEDNESDAY
from django.db import models
from django.utils.translation import gettext_lazy as _


class WEEKDAYS(models.IntegerChoices):
    MONDAY = 1, _("Lundi")
    TUESDAY = 2, _("Mardi")
    WEDNESDAY = 3, _("Mercredi")
    THURSDAY = 4, _("Jeudi")
    FRIDAY = 5, _("Vendredi")
    SATURDAY = 6, _("Samedi")
    SUNDAY = 7, _("Dimanche")
