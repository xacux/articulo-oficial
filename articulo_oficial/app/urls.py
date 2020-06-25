from rest_framework import routers
from app.views import ArticuloViewSet

router = routers.SimpleRouter()
router.register('productos',ArticuloViewSet)

urlpatterns = router.urls