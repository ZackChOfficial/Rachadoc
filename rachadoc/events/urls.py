from rest_framework import routers
from events.views import EventViewSet, AppointementViewSet, PersonalEventViewSet

router = routers.SimpleRouter()

router.register(r"event", EventViewSet)
router.register(r"appointement", AppointementViewSet)
router.register(r"personal-event", PersonalEventViewSet)

urlpatterns = router.urls
