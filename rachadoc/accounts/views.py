from rest_framework import viewsets
from accounts.serializers import PatientSerializer, DoctorSerializer, ReceptionistSerializer, UserSerializer
from accounts.models import Patient, Doctor, Receptionist, User
from rest_framework.response import Response
from rules.contrib.rest_framework import AutoPermissionViewSetMixin
from rest_framework.decorators import action
from clinic.models import Clinic
from common.models import Expertise
from core.lib.utils import get_object_or_none
from rest_framework import status
from core.lib.utils import getDoctorFromRequest, getReceptionistFromRequest
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.conf import settings

from core.lib.utils import get_user_profile
from django.shortcuts import redirect

User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=["get"])
    def me(self, request, *args, **kwargs):
        profile = get_user_profile(request.user)
        if profile == settings.DOCTOR:
            doctor = getDoctorFromRequest(request)
            serializer = DoctorSerializer(doctor)
            return Response({"profile": profile, **serializer.data})
        elif profile == settings.RECEPTIONIST:
            doctor = getDoctorFromRequest(request)
            serializer = ReceptionistSerializer(doctor)
            return Response({"profile": profile, **serializer.data})
        serializer = UserSerializer(request.user)
        data = {
            "profile": profile,
            **serializer.data,
        }
        return Response(data)


class PatientViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    permission_type_map = {**AutoPermissionViewSetMixin.permission_type_map, "all": "list"}

    @action(detail=False, methods=["get"])
    def all(self, request, *args, **kwargs):
        qs = self.filter_queryset(self.get_queryset())
        serialized = PatientSerializer(qs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        serialized_data = PatientSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        patient = Patient.objects.create(password="", **serialized_data.validated_data)
        return Response(PatientSerializer(patient).data)


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
        expertises_ids = request.data.get("expertises", None)
        expertises = list(Expertise.objects.filter(id__in=expertises_ids))
        if len(expertises) != len(expertises_ids):
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        serialized_data = DoctorSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        serialized_data = {
            **serialized_data.validated_data,
            "expertises": expertises,
        }
        doctor = Doctor.objects.create_user(**serialized_data)
        return Response(DoctorSerializer(doctor).data)

    @action(detail=True, methods=["patch"])
    def add_clinic(self, request, pk=None):
        doctor = self.get_object()
        clinic = get_object_or_none(Clinic, id=request.data.get("clinic"))
        data = {"amount": request.data.get("amount"), "title": "title example", "description": "description"}
        if clinic:
            doctor.clinics.add(clinic, through_defaults=data)
            return Response(DoctorSerializer(doctor).data)
        else:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def remove_clinic(self, request, pk=None):
        doctor = self.get_object()
        clinic = get_object_or_none(Clinic, id=request.data.get("clinic"))
        if clinic:
            doctor.clinics.remove(clinic)
            return Response(DoctorSerializer(doctor).data)
        else:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def add_expertise(self, request, pk=None):
        doctor = self.get_object()
        expertise = get_object_or_none(Expertise, id=request.data.get("expertise"))
        if expertise:
            doctor.expertises.add(expertise)
            return Response(DoctorSerializer(doctor).data)
        else:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    def remove_expertise(self, request, pk=None):
        doctor = self.get_object()
        expertise = get_object_or_none(Expertise, id=request.data.get("expertise"))
        if expertise:
            doctor.expertises.remove(expertise)
            return Response(DoctorSerializer(doctor).data)
        else:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class ReceptionistViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ReceptionistSerializer
    queryset = Receptionist.objects.all()

    permission_type_map = {**AutoPermissionViewSetMixin.permission_type_map, "receptionist_by_clinic": "list"}

    def create(self, request):
        clinic_id = request.data.get("clinic")
        doctor = getDoctorFromRequest(request)
        user: User = request.user
        if not doctor and not user.is_superuser:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        if doctor and not doctor.clinics.filter(id=clinic_id).exists():
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        serialized_data = ReceptionistSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        receptionist = Receptionist.objects.create_user(**serialized_data.validated_data)
        return Response(ReceptionistSerializer(receptionist).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data
        if "clinic" not in data:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def receptionist_by_clinic(self, request):
        clinic_id = request.query_params.get("clinic_id")
        if not clinic_id:
            return Response({"message": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        doctor = get_object_or_none(Doctor, id=self.request.user.id)
        if not doctor or not doctor.clinics.filter(id=clinic_id).exists():
            return Response({"message": "unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(clinic__id=clinic_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
