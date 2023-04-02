from rest_framework import viewsets
from rachadoc.clinic.models import Clinic
from rachadoc.clinic.serializers import ClinicSerializer
from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class ClinicViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "list": "list",
    }
