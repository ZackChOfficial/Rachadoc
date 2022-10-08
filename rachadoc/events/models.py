from django.db import models
from events.managers import EventManager, AppointementManager, PersonalManager


class Event(models.Model):
    object = EventManager()


class Appointement(Event):
    objects = AppointementManager()


class PersonalEvent(Event):
    objects = PersonalManager()
