from django.db import models
from common.managers import TarifManager, PictureManager, ExpertiseManager


class Tarif(models.Model):
    objects = TarifManager()


class Picture(models.Model):
    objects = PictureManager()


class Expertise(models.Model):
    objects = ExpertiseManager()
