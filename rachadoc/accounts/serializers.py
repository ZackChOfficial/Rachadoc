from rachadoc.accounts.models import Patient, Doctor, Receptionist
from rest_flex_fields import FlexFieldsModelSerializer
from rachadoc.clinic.serializers import ClinicSerializer
from rachadoc.common.serializers import ExpertiseSerializer
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
import re

User = get_user_model()


class GroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "name")


class UserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "cnie",
            "date_of_birth",
            "gender",
            "picture",
            "email_verified",
            "phone_verified",
        )


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
            "phone_number",
        )
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate_phone_number(self, value):
        pattern = "^(?:(?:(?:\+|00)212[\s]?(?:[\s]?\(0\)[\s]?)?)|0){1}(?:5[\s.-]?[2-3]|6[\s.-]?[13-9]){1}[0-9]{1}(?:[\s.-]?\d{2}){3}$"
        if value and not re.match(pattern, value):
            raise serializers.ValidationError(_("numero de telephone est invalid"))
        return value


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
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
            "expertises": {"read_only": True},
            "clinics": {"read_only": True},
        }


class ReceptionistSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Receptionist
        fields = (
            "id",
            "password",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "clinic",
            "is_active",
            "phone_number",
        )
        extra_kwargs = {"id": {"read_only": True}, "password": {"write_only": True}}
        expandable_fields = {
            "clinic": (ClinicSerializer),
        }
