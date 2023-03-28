from django.utils.translation import gettext_lazy as _

SCHEDULED = 1
DELIVERED = 2
DELIVERY_FAILURE = 4
OPTED_OUT = 3

STATUS_CHOICES = (
    (DELIVERED, _("Livré")),
    (DELIVERY_FAILURE, _("Échec de la livraison")),
    (OPTED_OUT, _("Désengagement")),
    (SCHEDULED, _("Programmé")),
)

EMAIL = 1
SMS = 2

CHANNEL_CHOICES = (
    (EMAIL, _("Email")),
    (SMS, _("SMS")),
)
