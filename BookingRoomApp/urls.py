from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('home/', views.home, name="home"),
    path('reservacion/', views.reservacion, name="reservacion"),
    path('administracion/servicios/', views.servicios, name="servicios"),
    path('administracion/trabajadores/', views.trabajadores, name="trabajadores"),
    path('administracion/salones/', views.salones, name="salones"),
    path('administracion/mobiliario/', views.mobiliario, name="mobiliario"),
    path('administracion/equipamiento/', views.equipamiento, name="equipamiento"),
    path('recepcion/historial/', views.historial_reservacion, name="historial_reservacion")
]