from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.IntegerChoices):
    UNKNOWN = 1, _("Inconnu")
    UPCOMING = 2, _("Prochain")
    ONGOING = 3, _("En cours")
    DONE = 4, _("Terminé")
    CANCELED = 5, _("Annulé")
