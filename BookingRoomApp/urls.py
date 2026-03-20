from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tipo-servicio', views.TipoServicioViewSet)

urlpatterns = router.urls + [
    path('login/', views.api_login, name='api_login'),
]
