from django.db import models
from rachadoc.notification.managers import NotificationManager
from django.utils.translation import gettext_lazy as _
import uuid
from rachadoc.notification.choices import STATUS_CHOICES, CHANNEL_CHOICES
from core.lib.mixins import BaseTimestampedModel


class Notification(BaseTimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.IntegerField(choices=STATUS_CHOICES)
    channel = models.IntegerField(choices=CHANNEL_CHOICES)
    scheduled_at = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)
    extra_data = models.JSONField(null=True, blank=True)
    target_id = models.CharField(max_length=4096)

    class Meta:
        abstract = True


class AppointementNotification(Notification):
    appointement = models.ForeignKey(
        "events.Appointement", on_delete=models.CASCADE, related_name="_appointement_notifs"
    )
    objects = NotificationManager()

    class Meta:
        unique_together = [
            "appointement",
            "channel",
            "scheduled_at",
        ]
