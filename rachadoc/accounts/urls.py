from rest_framework import routers
from accounts.views import PatientViewSet, DoctorViewSet, ReceptionistViewSet

router = routers.SimpleRouter()

router.register(r"patients", PatientViewSet)
router.register(r"doctors", DoctorViewSet)
router.register(r"receptionists", ReceptionistViewSet)

urlpatterns = router.urls
