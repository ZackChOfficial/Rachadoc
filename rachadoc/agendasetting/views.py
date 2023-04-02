from rest_framework import viewsets
from rachadoc.agendasetting.serializers import (
    ClinicAgendaSettingSerializer,
    DoctorAgendaSettingSerializer,
)
from rachadoc.agendasetting.models import ClinicAgendaSetting, DoctorAgendaSetting
from rachadoc.accounts.models import User, Doctor
from core.lib.utils import getDoctorFromRequest
from django.db.models import QuerySet
from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class ClinicAgendaSettingViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
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
        return queryset.filter(clinic__id__in=clinics)


class DoctorAgendaSettingViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
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
