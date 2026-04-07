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
router.register(r'encuesta', views.EncuestaViewSet)
router.register(r'registrestadoreserva', views.RegistrEstadReservaViewSet)
router.register(r'equipamiento', views.EquipamientoViewSet)
router.register(r'inventarioequipa', views.InventarioEquipaViewSet)
router.register(r'reservaequipa', views.ReservaEquipaViewSet)
router.register(r'servicio', views.ServicioViewSet)
router.register(r'pago', views.PagoViewSet)
router.register(r'mobiliario', views.MobiliarioViewSet)
router.register(r'inventario-mob', views.InventarioMobViewSet)
router.register(r'caracter-mobil', views.CaracterMobilViewSet)
router.register(r'salon', views.SalonViewSet)
router.register(r'estado-salon', views.RegistrEstadSalonViewSet)
router.register(r'montaje', views.MontajeViewSet)
router.register(r'montaje-mobiliario', views.MontajeMobiliarioViewSet)
router.register(r'reservacion', views.ReservacionViewSet)
router.register(r'reserva-servicio', views.ReservaServicioViewSet)
router.register(r'tipo-evento', views.TipoEventoViewSet)
router.register(r'tipo-montaje', views.TipoMontajeViewSet)
router.register(r'tipo-mobiliario', views.TipoMobiliarioViewSet)

urlpatterns = router.urls + [
    path('login/', views.api_login, name='api_login'),
    path('signup/', views.api_signup, name='api_signup'),
    path('flutter-login/', views.api_flutter_login, name='api_flutter_login'),
    path('buscar-reservacion/', views.BuscarReservacionView.as_view(), name='buscar_reservacion'),
    path('listar-reservacion/', views.ListarReservacionesView.as_view(), name='listar_reservaciones'),
    path('calendario-eventos/', views.LlenarCalendarioReservaciones.as_view(), name='calendario_eventos'),
    path('reservaciones-por-fecha/', views.ReservacionesPorFechaView.as_view(), name='reservaciones_por_fecha'),
    path('disponibilidad-salones/', views.DisponibilidadSalonesView.as_view(), name='disponibilidad_salones'),
    path('reservacion/<int:pk>/', views.DetalleReservacionView.as_view(), name='detalle_reservacion'),
    path('reservaciones-coordinador/', views.ListaReservacionesCoordinadorView.as_view(), name='reservaciones_coordinador'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('tipo-equipa/', views.ListTipoEquipa.as_view(), name='tipo_equipa'),
]
