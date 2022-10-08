from django.db import models
from clinic.managers import ClinicManager


class Clinic(models.Model):
    objects = ClinicManager()
