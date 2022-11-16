from rest_framework import viewsets
from agendasetting.serializers import (
    ClinicAgendaSettingSerializer,
    DoctorAgendaSettingSerializer,
)
from agendasetting.models import ClinicAgendaSetting, DoctorAgendaSetting
from accounts.models import User, Doctor
from core.lib.utils import getDoctorFromRequest
from django.db.models import QuerySet


class ClinicAgendaSettingViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicAgendaSettingSerializer
    queryset = ClinicAgendaSetting.objects.all()

    def get_queryset(self):
        user: User = self.request.user
        queryset: QuerySet = super().get_queryset()

        if user.is_superuser:
            return queryset
        doctor: Doctor = getDoctorFromRequest(self.request)
        if not doctor:
            return queryset.none()
        clinics = doctor.clinics.values_list("id", flat=True)
        return queryset.filter(clinic__id=clinics)


class DoctorAgendaSettingViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorAgendaSettingSerializer
    queryset = DoctorAgendaSetting.objects.all()

    def get_queryset(self):
        user: User = self.request.user
        queryset: QuerySet = super().get_queryset()

        if user.is_superuser:
            return queryset
        doctor: Doctor = getDoctorFromRequest(self.request)
        if not doctor:
            return queryset.none()
        return queryset.filter(doctor__id=doctor.id)
