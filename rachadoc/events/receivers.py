from django.db.models.signals import pre_save
from django.dispatch import receiver
from events.models import Appointement
from django.core.exceptions import ValidationError
from events.choices import Status
from django.utils import timezone


@receiver(pre_save, sender=Appointement)
def appointement_handler(sender, instance: Appointement, **kwargs):
    if instance.id:
        old_instance = Appointement.objects.get(id=instance.id)
        if old_instance.status > instance.status:
            raise ValidationError(
                f"Can't go back in status current status {old_instance.status} new status {instance.status}"
            )
        if instance.status == Status.WAITING:
            instance.waiting_examination = timezone.now()
        elif instance.status == Status.ONGOING:
            instance.start_examination = timezone.now()
        elif instance.status == Status.DONE:
            instance.end_examination = timezone.now()
