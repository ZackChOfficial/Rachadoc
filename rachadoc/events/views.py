from rest_framework import viewsets
from rachadoc.events.serializers import AppointementSerializer, BaseAppointementSerializer, PersonalSerializer
from rachadoc.events.models import Appointement, Personal as PersonalEvent
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from rest_framework import status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rachadoc.core.lib.utils import (
    get_clinic_from_user,
    get_doctor_from_user,
    getDoctorFromRequest,
    getReceptionistFromRequest,
    get_object_or_none,
    get_user_profile,
)
from rachadoc.accounts.models import Doctor, Patient
from rachadoc.events.filters import AppointementFilter
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import orjson
from django.utils import timezone
from datetime import timedelta
from rachadoc.events.choices import Status
from django.db.models import Q, Count
from django.conf import settings
from djangorestframework_camel_case.util import camelize
from datetime import timedelta
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()


class AppointementViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = AppointementSerializer
    queryset = Appointement.objects.all()
    ordering_fields = ["start", "end"]
    ordering = ["start", "end"]
    filterset_class = AppointementFilter

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "all": "list",
        "events_stats": "list",
        "patient_appointements": "list",
    }

    def get_queryset(self):
        clinic = None
        doctor = None
        profile = get_user_profile(self.request.user)
        self.profile = profile
        if profile == settings.SUPERUSER:
            return super().get_queryset()
        elif profile == settings.DOCTOR:
            doctor = get_doctor_from_user(self.request.user)
            clinic = doctor.clinics.first()
        elif profile == settings.RECEPTIONIST:
            clinic = get_clinic_from_user(self.request.user)
            doctor = Doctor.objects.get(clinics__in=[clinic.id])
        logger.info(f"Doctor: {doctor}  Clinic: {clinic}")
        self.doctor = doctor
        self.clinic = clinic
        return super().get_queryset().filter(clinic=clinic.id, doctor=doctor.id)

    def create(self, request, *args, **kwargs):
        serializedData = self.get_serializer(data=request.data)
        if not serializedData.is_valid():
            return Response(serializedData.errors, status=status.HTTP_400_BAD_REQUEST)
        patient = get_object_or_none(Patient, id=serializedData.data["patient"])
        if patient is None:
            return Response(_("Patient Introuvable"), status=status.HTTP_400_BAD_REQUEST)
        data = {
            **serializedData.data,
            "clinic": self.clinic,
            "doctor": self.doctor,
            "patient": patient,
            "creator": self.request.user,
        }
        appointement = Appointement(**data)
        appointement.save()
        appointementData = self.get_serializer(appointement).data
        # make appoitement data json friendly to send it through websocket
        data = orjson.loads(orjson.dumps(appointementData))
        async_to_sync(channel_layer.group_send)(str(self.clinic.id), {"type": "send_updates", "data": camelize(data)})
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        try:
            super().update(request, *args, **kwargs)
        except ValidationError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        appointement = self.get_object()
        serializer = self.get_serializer(appointement)
        data = orjson.loads(orjson.dumps(serializer.data))
        async_to_sync(channel_layer.group_send)(str(self.clinic.id), {"type": "send_updates", "data": camelize(data)})
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def all(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def patient_appointements(self, request, *args, **kwargs):
        patient_id = request.query_params.get("patient_id")
        qs = self.filter_queryset(self.get_queryset())
        qs = qs.filter(patient__id=patient_id)
        serializer = BaseAppointementSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(end__gte=timezone.now())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def events_stats(self, request, *args, **kwargs):
        now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = now + timedelta(days=1)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(status__in=[Status.DONE, Status.ONGOING, Status.WAITING])
        queryset = queryset.filter(Q(start__gte=now) & Q(start__lt=tomorrow))
        queryset = queryset.values("status").order_by("status").annotate(count=Count("status"))
        return Response(queryset)


class PersonalEventViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PersonalSerializer
    queryset = PersonalEvent.objects.all()
