from rest_framework import routers
from common.views import TarifViewSet, PictureViewSet, ExpertiseViewSet

router = routers.SimpleRouter()

router.register(r"tarif", TarifViewSet)
router.register(r"picture", PictureViewSet)
router.register(r"expertise", ExpertiseViewSet)

urlpatterns = router.urls
