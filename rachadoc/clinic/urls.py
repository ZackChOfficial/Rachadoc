from rest_framework import routers
from clinic.views import ClinicViewSet

router = routers.SimpleRouter()

router.register(r"", ClinicViewSet)

urlpatterns = router.urls
