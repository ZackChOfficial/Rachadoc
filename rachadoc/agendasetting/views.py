from rest_framework import viewsets
from agendasetting.serializers import (
    AgendaSettingSerializer,
    ClinicAgendaSettingSerializer,
    DoctorAgendaSettingSerializer,
)
from agendasetting.models import AgendaSetting, ClinicAgendaSetting, DoctorAgendaSetting


class AgendaSettingViewSet(viewsets.ModelViewSet):
    serializer_class = AgendaSettingSerializer
    queryset = AgendaSetting.objects.all()


class ClinicAgendaSettingViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicAgendaSettingSerializer
    queryset = ClinicAgendaSetting.objects.all()


class DoctorAgendaSettingViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorAgendaSettingSerializer
    queryset = DoctorAgendaSetting.objects.all()
