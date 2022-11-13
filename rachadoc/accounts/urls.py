from rest_framework import routers
from accounts.views import PatientViewSet, DoctorViewSet, ReceptionistViewSet

router = routers.SimpleRouter()

router.register(r"patient", PatientViewSet)
router.register(r"doctor", DoctorViewSet)
router.register(r"receptionist", ReceptionistViewSet)

urlpatterns = router.urls
