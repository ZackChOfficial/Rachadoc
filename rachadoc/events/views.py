from rest_framework import viewsets
from events.serializers import EventSerializer, AppointementSerializer, PersonalSerializer
from events.models import Event, Appointement, Personal as PersonalEvent
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from rest_framework import status
from rest_framework.response import Response

from core.lib.utils import getDoctorFromRequest, getReceptionistFromRequest, get_object_or_none
from accounts.models import Doctor, Patient
from events.filters import AppointementFilter
from rest_framework.decorators import action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import orjson

channel_layer = get_channel_layer()


class AppointementViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = AppointementSerializer
    queryset = Appointement.objects.all()
    ordering_fields = ["start", "end"]
    ordering = ["-start", "-end"]
    filterset_class = AppointementFilter

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "all": "list",
    }

    def create(self, request, *args, **kwargs):
        serializedData = AppointementSerializer(data=request.data)
        if not serializedData.is_valid():
            return Response(serializedData.errors, status=status.HTTP_400_BAD_REQUEST)
        doctor = getDoctorFromRequest(request)
        if not doctor:
            receptionist = getReceptionistFromRequest(request)
            clinic = receptionist.clinic
            doctor = Doctor.objects.get(clinics__in=[clinic.id])
        else:
            clinic = doctor.clinics.first()
        patient = get_object_or_none(Patient, serializedData.data["patient"])
        data = {**serializedData.data, "clinic": clinic, "doctor": doctor, "patient": patient}
        appointement = Appointement(**data)
        appointement.save()
        appointementData = AppointementSerializer(appointement).data
        data = orjson.loads(orjson.dumps(appointementData))
        async_to_sync(channel_layer.group_send)(str(clinic.id), {"type": "send_updates", "data": data})
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def all(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serialized = AppointementSerializer(qs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class PersonalEventViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PersonalSerializer
    queryset = PersonalEvent.objects.all()
