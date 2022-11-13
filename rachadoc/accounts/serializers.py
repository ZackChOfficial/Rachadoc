from accounts.models import Patient, Doctor, Receptionist
from rest_flex_fields import FlexFieldsModelSerializer
from clinic.serializers import ClinicSerializer
from common.serializers import ExpertiseSerializer
from django.contrib.auth.models import Group


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")


class PatientSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "city",
            "address",
            "CIVIL_STATUS",
            "insurance",
        )


class DoctorSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "description",
            "inp",
            "appointement_duration",
            "clinics",
            "expertises",
            "password",
            "groups",
        )
        expandable_fields = {
            "clinics": (ClinicSerializer, {"many": True}),
            "expertises": (ExpertiseSerializer, {"many": True}),
            "groups": (GroupSerializer, {"many": True}),
        }
        extra_kwargs = {"password": {"write_only": True}}


class ReceptionistSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Receptionist
        fields = ("id", "email", "first_name", "last_name", "date_joined", "clinic")
        expandable_fields = {
            "clinic": (ClinicSerializer),
        }
