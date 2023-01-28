from rest_flex_fields import FlexFieldsModelSerializer
from events.models import Appointement, Personal as PersonalEvent, Event
from clinic.serializers import ClinicSerializer
from accounts.serializers import PatientSerializer, DoctorSerializer


class EventSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "title", "start", "end", "status")


class AppointementSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Appointement
        fields = EventSerializer.Meta.fields + (
            "patient",
            "doctor",
            "clinic",
            "note_pre_appointement",
            "note_post_appointement",
        )
        extra_kwargs = {
            "doctor": {"read_only": True},
            "clinic": {"read_only": True},
        }
        expandable_fields = {"clinic": (ClinicSerializer), "patient": (PatientSerializer), "doctor": DoctorSerializer}


class PersonalSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = PersonalEvent
        fields = EventSerializer.Meta.fields + ("doctor", "note")
