from rest_framework import viewsets
from clinic.models import Clinic
from clinic.serializers import ClinicSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
