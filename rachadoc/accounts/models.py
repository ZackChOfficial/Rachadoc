from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from clinic.models import Clinic
from core.settings.business import DEFAULT_APPOINTEMENT_DURATION
from accounts.managers import BaseUserManager, PatientManager, DoctorManager, ReceptionistManager
from common.models import Expertise


class User(AbstractUser):
    """User model."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    GENDERS = (("UNKNOWN", _("Inconnu")), ("MALE", _("Homme")), ("FEMALE", _("Femme")))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_("address email"), unique=True)
    phone_number = models.CharField(_("numéro de téléphone"), max_length=255)
    cnie = models.CharField(_("carte nationale d'identité électronique"), max_length=255)
    date_of_birth = models.DateField(_("date de naissance"), null=True)
    gender = models.CharField(_("date de naissance"), choices=GENDERS, default="UNKNOWN", max_length=255)
    picture = models.URLField(_("photo de profil"))
    email_verified = models.BooleanField(_("email verifier"), default=False)
    phone_verified = models.BooleanField(_("numéro de téléphone verifier"), default=False)

    def __str__(self):
        return self.email


class Patient(User):
    CIVIL_STATUS = (
        ("UNKNOWN", _("Inconnu")),
        ("MARRIED", _("Marié")),
        ("Single", _("Célibataire")),
    )
    INSURANCES = (("UNKNOWN", _("Inconnu")),)

    city = models.CharField(_("ville de residence"), max_length=255)
    address = models.CharField(_("address"), max_length=2048)
    CIVIL_STATUS = models.CharField(_("État civil"), choices=CIVIL_STATUS, default="UNKNOWN", max_length=255)
    insurance = models.CharField(_("Mutuelle"), choices=INSURANCES, default="UNKNOWN", max_length=255)
    objects = PatientManager()


class Doctor(User):
    description = models.CharField(_("description"), max_length=4096)
    INP = models.CharField(_("INP"), max_length=127)
    appointement_duration = models.IntegerField(_("Durée du rendez-vous"), default=DEFAULT_APPOINTEMENT_DURATION)
    tarifs = models.ManyToManyField(Clinic, through="Tarif")
    expertises = models.ManyToManyField(Expertise)
    objects = DoctorManager()


class Receptionist(User):
    Clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    objects = ReceptionistManager()
