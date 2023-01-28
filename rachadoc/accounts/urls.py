from rest_framework import routers
from accounts.views import PatientViewSet, DoctorViewSet, ReceptionistViewSet, UserViewSet

router = routers.SimpleRouter()

router.register(r"patient", PatientViewSet)
router.register(r"doctor", DoctorViewSet)
router.register(r"receptionist", ReceptionistViewSet)
router.register(r"user", UserViewSet)

urlpatterns = router.urls
