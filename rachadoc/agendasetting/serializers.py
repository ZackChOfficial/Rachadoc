from rest_flex_fields import FlexFieldsModelSerializer
from agendasetting.models import AgendaSetting, ClinicAgendaSetting, DoctorAgendaSetting
from clinic.serializers import ClinicSerializer
from accounts.serializers import DoctorSerializer


class AgendaSettingSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = AgendaSetting
        fields = ("week_day", "from_date", "to_date")


class ClinicAgendaSettingSerializer(AgendaSettingSerializer):
    class Meta(AgendaSettingSerializer.Meta):
        model = ClinicAgendaSetting
        fields = AgendaSettingSerializer.Meta.fields + ("clinic",)
        expandable_fields = {"clinic": (ClinicSerializer)}


class DoctorAgendaSettingSerializer(AgendaSettingSerializer):
    class Meta(AgendaSettingSerializer.Meta):
        model = DoctorAgendaSetting
        fields = AgendaSettingSerializer.Meta.fields + ("doctor",)
        expandable_fields = {"doctor": (DoctorSerializer)}
