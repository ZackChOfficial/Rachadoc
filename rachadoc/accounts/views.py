from rest_framework import viewsets
from accounts.serializers import PatientSerializer, DoctorSerializer, ReceptionistSerializer
from accounts.models import Patient, Doctor, Receptionist
from rest_framework.response import Response
from rules.contrib.rest_framework import AutoPermissionViewSetMixin

from common.models import Expertise


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class DoctorViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "list": "list",
    }

    def create(self, request):
        expertises_ids = request.data.getlist("expertises", None)
        expertises = list(Expertise.objects.filter(id__in=expertises_ids))
        serialized_data = {
            "email": request.data.get("email", None),
            "description": request.data.get("description", None),
            "inp": request.data.get("inp", None),
            "expertises": expertises,
            "password": request.data.get("password", None),
        }
        doctor = Doctor.objects.create_user(**serialized_data)
        return Response(DoctorSerializer(doctor).data)


class ReceptionistViewSet(viewsets.ModelViewSet):
    serializer_class = ReceptionistSerializer
    queryset = Receptionist.objects.all()
