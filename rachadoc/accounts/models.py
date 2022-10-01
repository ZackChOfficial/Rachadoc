from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager as DjangoBaseUserManager
import uuid
from clinic.models import Clinic
from events.models import Appointement


class BaseUserManager(DjangoBaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


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


class Doctor(User):
    description = models.CharField(_("description"), max_length=4096)
    INP = models.CharField(_("INP"), max_length=127)
    Appointement


class Receptionist(User):
    Clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
