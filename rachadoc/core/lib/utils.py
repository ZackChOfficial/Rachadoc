from rachadoc.accounts.models import Doctor, Patient, Receptionist, User
from typing import Optional
from django.conf import settings


def getDoctorFromRequest(request) -> Optional[Doctor]:
    user: User = request.user
    if not user:
        return None
    try:
        return Doctor.objects.get(id=user.id)
    except Doctor.DoesNotExist:
        return None


def getReceptionistFromRequest(request) -> Optional[Receptionist]:
    user: User = request.user
    if not user:
        return None
    try:
        return Receptionist.objects.get(id=user.id)
    except Receptionist.DoesNotExist:
        return None


def get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def get_user_profile(user: User) -> Optional[str]:
    if user is None:
        return settings.ANONYMOUS
    elif user.is_superuser:
        return settings.SUPERUSER
    elif Doctor.objects.filter(id=user.id).exists():
        return settings.DOCTOR
    elif Patient.objects.filter(id=user.id).exists():
        return settings.PATIENT
    elif Receptionist.objects.filter(id=user.id).exists():
        return settings.RECEPTIONIST
    else:
        return settings.ANONYMOUS
