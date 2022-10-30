from accounts.models import Patient, Doctor, Receptionist
from rest_flex_fields import FlexFieldsModelSerializer
from clinic.serializers import ClinicSerializer
from common.serializers import ExpertiseSerializer


class PatientSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Patient
        fields = ("email", "first_name", "last_name", "date_joined", "city", "address", "CIVIL_STATUS", "insurance")


class DoctorSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "description",
            "INP",
            "appointement_duration",
            "clinics",
            "expertises",
        )
        expandable_fields = {
            "clinics": (ClinicSerializer, {"many": True}),
            "expertises": (ExpertiseSerializer, {"many": True}),
        }


class ReceptionistSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Receptionist
        fields = ("email", "first_name", "last_name", "date_joined", "clinic")
        expandable_fields = {
            "clinic": (ClinicSerializer),
        }
