from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('home/', views.Home.as_view(), name="home"),
    path('reservacion/', views.ReservacionView.as_view(), name="reservacion"),
    path('home/<int:pk>/json/', views.reservacion_detalle_json, name='reservacion_detalle_json'),
    path('reservacion/<int:pk>/', views.DetallesReservacionView.as_view(), name="reservacion"),
    path('administracion/servicios/', views.Servicios.as_view(), name="servicios"),
    # path('recepcion/historial/', views.historial_reservacion, name="historial_reservacion"),
    path('recepcion/historial/', views.HistorialReservacionViw.as_view(), name="historial_reservacion"),
    path('recepcion/historial/<int:pk>/json/', views.historial_detalle, name="historial_detalle_json"),
    path('almacen/inventario-equipamiento/', views.inventario_equipamiento, name="inventario_equipamiento"),
    path('almacen/inventario-mobiliario/', views.inventario_mobiliario, name="inventario_mobiliario"),
    path('recepcion/pagos/', views.pagos, name="pagos"),
    path('administracion/estadisticas/', views.estadisticas, name="estadisticas"),
    path('administracion/trabajadores/', views.trabajadores, name="trabajadores"),
    path('administracion/trabajadores/registrar/', views.registrar_trabajador, name="registrar_trabajador"),
    path('administracion/salones/', views.Salones.as_view(), name="salones"),
    path('administracion/mobiliario/', views.Mobiliarios.as_view(), name="mobiliario"),
    path('administracion/equipamiento/', views.Equipamientos.as_view(), name="equipamiento"),
]
