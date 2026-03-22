from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tipo-servicio', views.TipoServicioViewSet)
router.register(r'rol', views.RolViewSet)
router.register(r'estado-cuenta', views.EstadoCuentaViewSet)
router.register(r'tipo-cliente', views.TipoClienteViewSet)
router.register(r'cuenta', views.CuentaViewSet)
router.register(r'trabajador', views.TrabajadorViewSet)
router.register(r'datos-cliente', views.DatosClienteViewSet)

urlpatterns = router.urls + [
    path('login/', views.api_login, name='api_login'),
    path('signup/', views.api_signup, name='api_signup'),
    path('flutter-login/', views.api_flutter_login, name='api_flutter_login'),
]
