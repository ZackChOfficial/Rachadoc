from rest_framework import viewsets
from agendasetting.serializers import (
    AgendaSettingSerializer,
    ClinicAgendaSettingSerializer,
    DoctorAgendaSettingSerializer,
)
from agendasetting.models import ClinicAgendaSetting, DoctorAgendaSetting


class ClinicAgendaSettingViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicAgendaSettingSerializer
    queryset = ClinicAgendaSetting.objects.all()


class DoctorAgendaSettingViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorAgendaSettingSerializer
    queryset = DoctorAgendaSetting.objects.all()
