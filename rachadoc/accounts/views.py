from rest_framework import viewsets
from accounts.serializers import PatientSerializer, DoctorSerializer, ReceptionistSerializer
from accounts.models import Patient, Doctor, Receptionist, User
from rest_framework.response import Response
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from django.db import transaction
from rest_framework.decorators import action
from clinic.models import Clinic
from common.models import Expertise
from core.lib.utils import get_object_or_none
from rest_framework import status

from core.lib.utils import getDoctorFromRequest


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class DoctorViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "list": "list",
        "add_clinic": "list",
        "remove_clinic": "list",
        "add_expertise": "change",
        "remove_expertise": "change",
    }

    def create(self, request):
        expertises_ids = request.data.getlist("expertises", None)
        expertises = list(Expertise.objects.filter(id__in=expertises_ids))
        serialized_data = {
            **request.data,
            "email": request.data.get("email", None),
            "description": request.data.get("description", None),
            "inp": request.data.get("inp", None),
            "expertises": expertises,
            "password": request.data.get("password", None),
        }
        doctor = Doctor.objects.create_user(**serialized_data)
        return Response(DoctorSerializer(doctor).data)

    @action(detail=True, methods=["patch"])
    def add_clinic(self, request, pk=None):
        doctor = self.get_object()
        clinic = get_object_or_none(Clinic, request.data.get("clinic"))
        data = {"amount": request.data.get("amount"), "title": "title example", "description": "description"}
        if clinic:
            doctor.clinics.add(clinic, through_defaults=data)
            return Response(DoctorSerializer(doctor).data)
        else:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def remove_clinic(self, request, pk=None):
        doctor = self.get_object()
        clinic = get_object_or_none(Clinic, request.data.get("clinic"))
        if clinic:
            doctor.clinics.remove(clinic)
            return Response(DoctorSerializer(doctor).data)
        else:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def add_expertise(self, request, pk=None):
        doctor = self.get_object()
        expertise = get_object_or_none(Expertise, request.data.get("expertise"))
        if expertise:
            doctor.expertises.add(expertise)
            return Response(DoctorSerializer(doctor).data)
        else:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def remove_expertise(self, request, pk=None):
        doctor = self.get_object()
        expertise = get_object_or_none(Expertise, request.data.get("expertise"))
        if expertise:
            doctor.expertises.remove(expertise)
            return Response(DoctorSerializer(doctor).data)
        else:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class ReceptionistViewSet(viewsets.ModelViewSet):
    serializer_class = ReceptionistSerializer
    queryset = Receptionist.objects.all()

    def create(self, request):
        clinic_id = request.data.get("clinic")
        doctor = getDoctorFromRequest(request)
        user: User = request.user
        if not doctor and not user.is_superuser:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        if doctor and not doctor.clinics.filter(id=clinic_id).exists():
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)
