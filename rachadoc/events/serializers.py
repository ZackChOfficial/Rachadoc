from rest_flex_fields import FlexFieldsModelSerializer
from events.models import Appointement, Personal as PersonalEvent, Event


class EventSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Event
        fields = ("patient", "doctor", "clinic", "note_pre_appointement", "note_post_appointement")


class AppointementSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Appointement
        fields = ("patient", "doctor", "clinic", "note_pre_appointement", "note_post_appointement")


class PersonalSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = PersonalEvent
        fields = ("doctor", "note", "clinic", "note_pre_appointement", "note_post_appointement")
