from celery import shared_task
from django.utils import timezone
from django.conf import settings
from rachadoc.notification.utils import send_appointement_email_notification
from rachadoc.notification.models import AppointementNotification
import rachadoc.notification.choices as choices
from datetime import timedelta
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


@shared_task()
def t_send_apointement_reminder():
    logger.info("sending appointements reminders")
    now = timezone.now()
    past_appoitement = now - timedelta(minutes=settings.APPOINTEMENT_NOTIF_DELTA)  # to filter out passed appoints
    email_notifications = AppointementNotification.objects.filter(
        status=choices.SCHEDULED, scheduled_at__lte=now, scheduled_at__gt=past_appoitement, channel=choices.EMAIL
    )
    sms_notifications = AppointementNotification.objects.filter(
        status=choices.SCHEDULED, scheduled_at__lte=now, scheduled_at__gt=past_appoitement, channel=choices.SMS
    )
    # disactivate old appoints
    AppointementNotification.objects.filter(status=choices.SCHEDULED, scheduled_at__lte=past_appoitement).update(
        status=choices.DISABLED
    )

    for notification in email_notifications:
        send_appointement_email_notification(notification)

    for notification in sms_notifications:
        pass  # TODO send sms notifs

    logger.info("appointements reminders sent")


@shared_task()
def t_send_excel_export():
    pass
