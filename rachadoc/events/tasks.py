from celery import shared_task
from django.utils import timezone
from notification.utils import send_appointement_email_notification
from notification.models import AppointementNotification
import notification.choices as choices
from django.conf import settings


@shared_task()
def t_send_apointement_reminder():
    print("t_send_apointement_reminder is running")
    email_notifications = AppointementNotification.objects.filter(
        status=choices.SCHEDULED, scheduled_at__lte=timezone.now(), channel=choices.EMAIL
    )
    sms_notifications = AppointementNotification.objects.filter(
        status=choices.SCHEDULED, scheduled_at__lte=timezone.now(), channel=choices.SMS
    )
    print(email_notifications)
    for notification in email_notifications:
        print("enter")
        send_appointement_email_notification(notification)

    for notification in sms_notifications:
        pass  # TODO send sms notifs


@shared_task()
def t_send_excel_export():
    pass
