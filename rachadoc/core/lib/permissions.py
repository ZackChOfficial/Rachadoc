from rules.predicates import predicate


@predicate
def is_obj_owner(user, obj):
    return user.id == obj.id


@predicate
def is_doctor(user):
    from rachadoc.accounts.models import Doctor

    return Doctor.objects.filter(id=user.id).exists()


@predicate
def is_receptionist(user):
    from rachadoc.accounts.models import Receptionist

    return Receptionist.objects.filter(id=user.id).exists()


@predicate
def is_doctor_and_same_clinic(user, obj):
    from rachadoc.accounts.models import Doctor
    from rachadoc.core.lib.utils import get_object_or_none

    doctor = get_object_or_none(Doctor, id=user.id)
    if not doctor:
        return False
    return doctor.clinics.filter(id=obj.clinic.id).exists()


@predicate
def is_event_owner(user, obj):
    from rachadoc.accounts.models import Doctor

    is_doctor = Doctor.objects.filter(id=user.id).exists()
    if not is_doctor:
        return False
    return obj.doctor.id == user.id


@predicate
def is_receptionist_same_clinic(user, obj):
    from rachadoc.accounts.models import Receptionist
    from rachadoc.core.lib.utils import get_object_or_none

    receptionist: Receptionist = get_object_or_none(Receptionist, id=user.id)
    if not receptionist:
        return False
    return obj.clinic.id == receptionist.clinic.id


@predicate
def is_doctor_and_tarif_owner(user, obj):
    from rachadoc.accounts.models import Doctor

    is_doctor = Doctor.objects.filter(id=user.id).exists()
    if not is_doctor:
        return False
    return obj.doctor.id == user.id


@predicate
def is_doctor_and_AgendaSetting_owner(user, obj):
    from rachadoc.accounts.models import Doctor

    is_doctor = Doctor.objects.filter(id=user.id).exists()
    if not is_doctor:
        return False
    return obj.doctor.id == user.id
