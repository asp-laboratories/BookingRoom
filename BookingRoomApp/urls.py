from rest_framework.routers import DefaultRouter
from .views import TipoServicioViewSet

router = DefaultRouter()
router.register(r'tipo-servicio', TipoServicioViewSet)

urlpatterns = router.urls
