from django.db.models.signals import post_save
from django.dispatch import receiver
from rachadoc.events.models import Appointement
from rachadoc.notification.utils import (
    create_or_update_email_appointement_notification,
    create_or_update_sms_appointement_notification,
)
from rachadoc.notification.exceptions import NotificationsNotCreated
from rachadoc.notification.models import AppointementNotification
import rachadoc.notification.choices as choices


def delete_notification(appointement: Appointement, channel):
    return AppointementNotification.objects.filter(appointement__id=appointement.id, channel=channel).delete()


@receiver(post_save, sender=Appointement)
def notification_handler(sender, instance: Appointement, **kwargs):
    print("called")
    if instance.send_email:
        try:
            create_or_update_email_appointement_notification(instance)
        except NotificationsNotCreated:
            # TODO log info
            pass
    else:
        delete_notification(instance, choices.EMAIL)

    if instance.send_sms:
        try:
            create_or_update_sms_appointement_notification(instance)
        except NotificationsNotCreated:
            # TODO log info
            pass
    else:
        delete_notification(instance, choices.SMS)
