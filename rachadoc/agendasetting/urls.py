from rest_framework import routers
from rachadoc.agendasetting.views import ClinicAgendaSettingViewSet, DoctorAgendaSettingViewSet

router = routers.SimpleRouter()

router.register(r"clinic", ClinicAgendaSettingViewSet)
router.register(r"doctor", DoctorAgendaSettingViewSet)

urlpatterns = router.urls
