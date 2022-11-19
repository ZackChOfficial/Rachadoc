from rest_framework import routers
from events.views import EventViewSet, AppointementViewSet, PersonalEventViewSet
from django.urls import re_path

router = routers.SimpleRouter()

router.register(r"event", EventViewSet)
router.register(r"appointement", AppointementViewSet)
router.register(r"personal-event", PersonalEventViewSet)

urlpatterns = router.urls


websocket_urlpatterns = []
