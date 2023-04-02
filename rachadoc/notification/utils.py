from datetime import datetime
from typing import Tuple
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import EmailMessage
from django.conf import settings

from rachadoc.notification.models import AppointementNotification
from rachadoc.notification.exceptions import NotificationsNotCreated

from rachadoc.events.models import Appointement
import notification.choices as choices
from rachadoc.notification.models import AppointementNotification
from datetime import timedelta, datetime
from rachadoc.notification.exceptions import NotificationsNotCreated
from core.lib.utils import get_object_or_none


def create_or_update_appointement_notification(
    appointement: Appointement, channel: choices.CHANNEL_CHOICES
) -> AppointementNotification:
    """
    This function will generate a notification.
    """
    start = appointement.start
    if type(start) == str:
        start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
    scheduled_at: datetime = start - timedelta(hours=1)
    notification = get_object_or_none(
        AppointementNotification, status=choices.SCHEDULED, channel=channel, appointement__id=appointement.id
    )
    if not notification:
        notification = AppointementNotification.objects.create(
            status=choices.SCHEDULED,
            channel=channel,
            appointement=appointement,
            scheduled_at=scheduled_at,
            target_id=appointement.patient.email,
        )
    else:
        notification.scheduled_at = scheduled_at
        notification.target_id = appointement.patient.email
        notification.save(update_fields=["scheduled_at", "target_id"])
    return notification


def create_or_update_email_appointement_notification(
    appointement: Appointement,
) -> AppointementNotification:
    """
    This function will generate an email notification.
    """
    if not appointement.patient.email:
        raise NotificationsNotCreated("user doesn't have email")

    # TODO check if user is opt out

    return create_or_update_appointement_notification(appointement, choices.EMAIL)


def create_or_update_sms_appointement_notification(
    appointement: Appointement,
) -> AppointementNotification:
    """
    This function will generate an email notification.
    """
    if not appointement.patient.phone_number:
        raise NotificationsNotCreated("user doesn't have phone number")

    # TODO check if user is opt out

    return create_or_update_appointement_notification(appointement, choices.SMS)


def send_email_notification(notification: AppointementNotification, template_id, template_data) -> str:
    """
    Send email notifications to the target email.

    Returns:
        str: Whether the email has successfully sent, or an error message.
    """
    try:
        print("sending email")
        email = EmailMessage(to=[notification.target_id])
        email.template_id = template_id
        email.from_email = None
        email.merge_global_data = template_data
        email.send()
    except Exception as e:
        notification.status = choices.DELIVERY_FAILURE
        notification.save()
        return f"Email could not be sent: {e}"

    # If everything is fine, we update the notification
    # to DELIVERED
    notification.status = choices.DELIVERED
    notification.delivered_at = timezone.now()
    notification.save()
    return "Email Successfully Sent"


def send_appointement_email_notification(notification: AppointementNotification) -> str:
    """
    Send email notifications to the target email.

    Returns:
        str: Whether the email has successfully sent, or an error message.
    """
    template_id = settings.APPOINTEMENT_NOTIFICATION_TEMPLATE_ID
    PATIENT_FULLNAME = f"{notification.appointement.patient.first_name} {notification.appointement.patient.last_name}"
    DOCTOR_FULLNAME = f"{notification.appointement.doctor.first_name} {notification.appointement.doctor.last_name}"
    template_data = {
        "PATIENT_FULLNAME": PATIENT_FULLNAME,
        "DOCTOR_FULLNAME": DOCTOR_FULLNAME,
        # TODO add other template data
    }
    return send_email_notification(notification, template_id, template_data)
