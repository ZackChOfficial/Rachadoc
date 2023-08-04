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
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Appointement)
def notification_handler(sender, instance: Appointement, **kwargs):
    if instance.send_email:
        try:
            create_or_update_email_appointement_notification(instance)
            logger.info("email notification created and will be sent in the next cronjob round")
        except NotificationsNotCreated:
            logger.warning(f"Email notification for appointement {instance.id} was not created")
        except Exception as e:
            logger.error(repr(e))
    else:
        AppointementNotification.objects.delete_by_appointement(instance, channel=choices.EMAIL)

    if instance.send_sms:
        try:
            create_or_update_sms_appointement_notification(instance)
            logger.info("sms notification created and will be sent in the next cronjob round")
        except NotificationsNotCreated:
            logger.warning(f"SMS notification for appointement {instance.id} was not created")
        except Exception as e:
            logger.error(repr(e))
    else:
        AppointementNotification.objects.delete_by_appointement(instance, channel=choices.SMS)
