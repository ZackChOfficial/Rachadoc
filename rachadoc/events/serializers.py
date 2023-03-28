from rest_flex_fields import FlexFieldsModelSerializer
from events.models import Appointement, Personal as PersonalEvent, Event
from clinic.serializers import ClinicSerializer
from accounts.serializers import PatientSerializer, DoctorSerializer, UserSerializer
from rest_framework import serializers


class EventSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "title", "start", "end", "status")


class AppointementSerializer(FlexFieldsModelSerializer):
    patient = serializers.SerializerMethodField()

    class Meta:
        model = Appointement
        fields = EventSerializer.Meta.fields + (
            "patient",
            "doctor",
            "clinic",
            "note_pre_appointement",
            "note_post_appointement",
            "creator",
            "send_sms",
            "send_email",
        )
        extra_kwargs = {
            "doctor": {"read_only": True},
            "clinic": {"read_only": True},
            "creator": {"read_only": True},
        }
        expandable_fields = {"clinic": (ClinicSerializer), "doctor": DoctorSerializer}

    def get_patient(self, obj):
        if isinstance(obj, Appointement):
            fields = ["id", "first_name", "last_name", "email", "phone_number"]
            patient = PatientSerializer(instance=obj.patient, read_only=True, fields=fields)
            return patient.data
        return self.initial_data["patient"]


class PersonalSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = PersonalEvent
        fields = EventSerializer.Meta.fields + ("doctor", "note")
