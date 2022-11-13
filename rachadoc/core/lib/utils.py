from accounts.models import Doctor, Patient, Receptionist, User
from typing import Optional


def getDoctorFromRequest(request) -> Optional[Doctor]:
    user: User = request.user
    if not user:
        return None
    try:
        return Doctor.objects.get(id=user.id)
    except Doctor.DoesNotExist:
        return None


def getReceptionistFromRequest(request) -> Optional[Doctor]:
    user: User = request.user
    if not user:
        return None
    try:
        return Receptionist.objects.get(user__id=user.id)
    except Receptionist.DoesNotExist:
        return None
