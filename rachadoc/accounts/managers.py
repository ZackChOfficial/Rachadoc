from django.db import models, transaction
from django.contrib.auth.models import BaseUserManager as DjangoBaseUserManager
from django.contrib.auth.models import Group

from clinic.models import Clinic


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


class PatientQuerySet(models.QuerySet):
    pass


class PatientManager(BaseUserManager):
    def get_queryset(self):
        return PatientQuerySet(self.model, using=self._db)


class DoctorQuerySet(models.QuerySet):
    pass


class DoctorManager(BaseUserManager):
    def get_queryset(self):
        return DoctorQuerySet(self.model, using=self._db)

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a doctor User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        expertises = extra_fields.pop("expertises", [])
        clinics = extra_fields.pop("clinics", [])
        with transaction.atomic():
            doctor = self.model(email=email, **extra_fields)
            doctor.set_password(password)
            doctor.save(using=self._db)
            doctor_group, _ = Group.objects.get_or_create(name="Doctor")
            doctor.groups.add(doctor_group.id)
            doctor.expertises.set(expertises)
            doctor.clinics.set(clinics)
        return doctor


class ReceptionistQuerySet(models.QuerySet):
    pass


class ReceptionistManager(BaseUserManager):
    def get_queryset(self):
        return ReceptionistQuerySet(self.model, using=self._db)

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a receptionist User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        clinic_id = extra_fields.pop("clinic")
        with transaction.atomic():
            receptionist = self.model(email=email, **extra_fields)
            receptionist.set_password(password)
            clinic = Clinic.objects.only("id").get(id=clinic_id)
            receptionist.clinic = clinic
            receptionist.save(using=self._db)
            receptionist_group, _ = Group.objects.get_or_create(name="Receptionist")
            receptionist.groups.add(receptionist_group.id)
        return receptionist
