from rules.predicates import predicate


@predicate
def is_obj_owner(user, obj):
    return user.id == obj.id


@predicate
def is_doctor(user):
    from accounts.models import Doctor

    return Doctor.objects.filter(id=user.id).exists()


@predicate
def is_receptionist(user):
    from accounts.models import Receptionist

    return Receptionist.objects.filter(id=user.id).exists()


@predicate
def is_doctor_and_same_clinic(user, obj):
    from accounts.models import Doctor

    is_doctor = Doctor.objects.filter(id=user.id).exists()
    if not is_doctor:
        return False
    return user.clinics.filter(id=obj.clinic.id).exists()


@predicate
def is_event_owner(user, obj):
    from accounts.models import Doctor

    is_doctor = Doctor.objects.filter(id=user.id).exists()
    if not is_doctor:
        return False
    return obj.doctor.id == user.id


@predicate
def is_receptionist_same_clinic(user, obj):
    from accounts.models import Receptionist

    is_receptionist: Receptionist = Receptionist.objects.filter(id=user.id).exists()
    if not is_receptionist:
        return False
    return obj.clinic.id == is_receptionist.clinic.id


@predicate
def is_doctor_and_tarif_owner(user, obj):
    from accounts.models import Doctor

    is_doctor = Doctor.objects.filter(id=user.id).exists()
    if not is_doctor:
        return False
    return obj.doctor.id == user.id
