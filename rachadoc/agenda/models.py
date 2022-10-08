from django.db import models
from agenda.managers import AgendaManager


class Agenda(models.Model):
    objects = AgendaManager()
