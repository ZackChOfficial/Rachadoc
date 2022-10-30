from rest_framework import viewsets
from events.serializers import EventSerializer, AppointementSerializer, PersonalSerializer
from events.models import Event, Appointement, Personal as PersonalEvent


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class AppointementViewSet(viewsets.ModelViewSet):
    serializer_class = AppointementSerializer
    queryset = Appointement.objects.all()


class PersonalEventViewSet(viewsets.ModelViewSet):
    serializer_class = PersonalSerializer
    queryset = PersonalEvent.objects.all()
