from rest_framework import viewsets
from clinic.models import Clinic
from clinic.serializers import ClinicSerializer
from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class ClinicViewSet(viewsets.ModelViewSet):
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        "list": "list",
    }
