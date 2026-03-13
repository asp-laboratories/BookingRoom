from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('home/', views.home, name="home"),
    path('reservacion/', views.reservacion, name="reservacion"),
    path('administracion/servicios/', views.servicios, name="servicios"),
    path('recepcion/historial/', views.historial_reservacion, name="historial_reservacion"),
    path('almacen/inventario-equipamiento/', views.inventario_equipamiento, name="inventario_equipamiento"),
    path('almacen/inventario-mobiliario/', views.inventario_mobiliario, name="inventario_mobiliario"),
    path('recepcion/pagos/', views.pagos, name="pagos"),
    path('administracion/estadisticas/', views.estadisticas, name="estadisticas"),
    path('administracion/trabajadores/', views.trabajadores, name="trabajadores"),
    path('administracion/salones/', views.salones, name="salones"),
    path('administracion/mobiliario/', views.mobiliario, name="mobiliario"),
    path('administracion/equipamiento/', views.equipamiento, name="equipamiento"),
]