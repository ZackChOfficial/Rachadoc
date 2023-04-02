from rest_framework import routers
from rachadoc.events.views import AppointementViewSet, PersonalEventViewSet
from django.urls import re_path
from rachadoc.events.consumers import EventstConsumer

router = routers.SimpleRouter()

router.register(r"appointement", AppointementViewSet)
router.register(r"personal-event", PersonalEventViewSet)

urlpatterns = router.urls


websocket_urlpatterns = [re_path(r"ws/event/", EventstConsumer.as_asgi(), name="event-consumer")]
