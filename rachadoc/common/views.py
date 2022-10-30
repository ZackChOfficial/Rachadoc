from rest_framework import viewsets
from common.models import Tarif, Picture, Expertise
from common.serializers import TarifSerializer, PictureSerializer, ExpertiseSerializer


class TarifViewSet(viewsets.ModelViewSet):
    serializer_class = TarifSerializer
    queryset = Tarif.objects.all()


class PictureViewSet(viewsets.ModelViewSet):
    serializer_class = PictureSerializer
    queryset = Picture.objects.all()


class ExpertiseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpertiseSerializer
    queryset = Expertise.objects.all()
