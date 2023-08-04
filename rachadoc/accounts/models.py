from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from rachadoc.core.settings.business import DEFAULT_APPOINTEMENT_DURATION
from rachadoc.accounts.managers import BaseUserManager, PatientManager, DoctorManager, ReceptionistManager
from rachadoc.common.models import Expertise
from rachadoc.accounts.choices import GENDERS, CIVIL_STATUS, INSURANCES
import rules
from rules.contrib.models import RulesModelMixin, RulesModelBase
from auditlog.registry import auditlog

from rachadoc.core.lib.permissions import is_obj_owner, is_doctor, is_doctor_and_same_clinic


class User(DjangoAbstractUser, RulesModelMixin, metaclass=RulesModelBase):
    """AbstractUser model."""

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_("address email"), unique=True)
    phone_number = models.CharField(_("numéro de téléphone"), max_length=255, null=True, blank=True)
    email_verified = models.BooleanField(_("email verifier"), default=False)
    phone_verified = models.BooleanField(_("numéro de téléphone verifier"), default=False)
    gender = models.IntegerField(_("date de naissance"), choices=GENDERS.choices, default=GENDERS.UNKNOWN)
    date_of_birth = models.DateField(_("date de naissance"), null=True, blank=True)

    def __str__(self):
        return self.email


class Patient(User):
    city = models.CharField(_("ville de residence"), max_length=255, blank=True, null=True)
    address = models.CharField(_("address"), max_length=2048, blank=True, null=True)
    CIVIL_STATUS = models.IntegerField(_("État civil"), choices=CIVIL_STATUS.choices, default=CIVIL_STATUS.UNKNOWN)
    insurance = models.IntegerField(_("Mutuelle"), choices=INSURANCES.choices, default=INSURANCES.UNKNOWN)
    clinics = models.ManyToManyField("clinic.Clinic", related_name="patients")
    objects = PatientManager()

    class Meta:
        rules_permissions = {
            "add": rules.always_allow,
            "change": rules.always_allow,
            "delete": rules.is_superuser,
            "view": rules.always_allow,
            "list": rules.always_allow,
        }


class Doctor(User):
    description = models.CharField(_("description"), max_length=4096)
    inp = models.CharField(_("INP"), max_length=127)
    appointement_duration = models.IntegerField(_("Durée du rendez-vous"), default=DEFAULT_APPOINTEMENT_DURATION)
    clinics = models.ManyToManyField("clinic.Clinic", through="common.Tarif")
    expertises = models.ManyToManyField(Expertise)
    cnie = models.CharField(_("carte nationale d'identité électronique"), max_length=255)
    picture = models.URLField(_("photo de profil"))
    objects = DoctorManager()

    class Meta:
        rules_permissions = {
            "add": rules.is_superuser,
            "change": (rules.is_superuser | is_obj_owner),
            "delete": rules.is_superuser,
            "view": (rules.is_superuser | is_obj_owner),
            "list": rules.is_superuser,
        }


class Receptionist(User):
    clinic = models.ForeignKey("clinic.Clinic", on_delete=models.CASCADE)
    cnie = models.CharField(_("carte nationale d'identité électronique"), max_length=255)
    picture = models.URLField(_("photo de profil"))
    objects = ReceptionistManager()

    class Meta:
        rules_permissions = {
            "add": (rules.is_superuser | is_doctor),
            "change": (rules.is_superuser | is_doctor_and_same_clinic),
            "delete": (rules.is_superuser | is_doctor_and_same_clinic),
            "view": (rules.is_superuser | is_doctor_and_same_clinic),
            "list": rules.is_superuser | is_doctor,
        }


auditlog.register(User)
auditlog.register(Patient)
auditlog.register(Doctor)
auditlog.register(Receptionist)
