from rest_framework import viewsets
from accounts.serializers import PatientSerializer, DoctorSerializer, ReceptionistSerializer
from accounts.models import Patient, Doctor, Receptionist


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()


class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()


class ReceptionistViewSet(viewsets.ModelViewSet):
    serializer_class = ReceptionistSerializer
    queryset = Receptionist.objects.all()
