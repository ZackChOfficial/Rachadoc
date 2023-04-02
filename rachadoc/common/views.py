from rest_framework import viewsets
from rachadoc.common.models import Tarif, Picture, Expertise
from rachadoc.common.serializers import TarifSerializer, PictureSerializer, ExpertiseSerializer
from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class TarifViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = TarifSerializer
    queryset = Tarif.objects.all()


class PictureViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PictureSerializer
    queryset = Picture.objects.all()


class ExpertiseViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ExpertiseSerializer
    queryset = Expertise.objects.all()
