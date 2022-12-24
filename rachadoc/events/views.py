from rest_framework import viewsets
from events.serializers import EventSerializer, AppointementSerializer, PersonalSerializer
from events.models import Event, Appointement, Personal as PersonalEvent
from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class EventViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class AppointementViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = AppointementSerializer
    queryset = Appointement.objects.all()


class PersonalEventViewSet(AutoPermissionViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PersonalSerializer
    queryset = PersonalEvent.objects.all()
