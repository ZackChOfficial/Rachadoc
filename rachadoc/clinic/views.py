from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from clinic.models import Clinic
from clinic.serializers import ClinicSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()

    def get_queryset(self):
        return super().get_queryset()
