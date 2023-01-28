from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.IntegerChoices):
    UNKNOWN = 1, _("Inconnu")
    UPCOMING = 2, _("Planifie")
    WAITING = 3, _("En Attente")
    ONGOING = 4, _("En cours")
    DONE = 5, _("Terminé")
    CANCELED = 6, _("Annulé")
