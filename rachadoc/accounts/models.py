from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from core.settings.business import DEFAULT_APPOINTEMENT_DURATION
from accounts.managers import BaseUserManager, PatientManager, DoctorManager, ReceptionistManager
from common.models import Expertise
from accounts.choices import GENDERS, CIVIL_STATUS, INSURANCES


class User(AbstractUser):
    """User model."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_("address email"), unique=True)
    phone_number = models.CharField(_("numéro de téléphone"), max_length=255)
    cnie = models.CharField(_("carte nationale d'identité électronique"), max_length=255)
    date_of_birth = models.DateField(_("date de naissance"), null=True)
    gender = models.IntegerField(_("date de naissance"), choices=GENDERS.choices, default=GENDERS.UNKNOWN)
    picture = models.URLField(_("photo de profil"))
    email_verified = models.BooleanField(_("email verifier"), default=False)
    phone_verified = models.BooleanField(_("numéro de téléphone verifier"), default=False)

    def __str__(self):
        return self.email


class Patient(User):
    city = models.CharField(_("ville de residence"), max_length=255)
    address = models.CharField(_("address"), max_length=2048)
    CIVIL_STATUS = models.IntegerField(_("État civil"), choices=CIVIL_STATUS.choices, default=CIVIL_STATUS.UNKNOWN)
    insurance = models.IntegerField(_("Mutuelle"), choices=INSURANCES.choices, default=INSURANCES.UNKNOWN)
    objects = PatientManager()


class Doctor(User):
    description = models.CharField(_("description"), max_length=4096)
    INP = models.CharField(_("INP"), max_length=127)
    appointement_duration = models.IntegerField(_("Durée du rendez-vous"), default=DEFAULT_APPOINTEMENT_DURATION)
    clinics = models.ManyToManyField("clinic.Clinic", through="common.Tarif")
    expertises = models.ManyToManyField(Expertise)
    objects = DoctorManager()


class Receptionist(User):
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.CASCADE)
    objects = ReceptionistManager()
