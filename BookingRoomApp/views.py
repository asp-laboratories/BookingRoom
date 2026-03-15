from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import TipoServicio
from .serializers import TipoServicioSerializer

class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer


# Create your views here.
def login(request):
    return render(request, 'BookingRoomApp/login.html')

def sign_up(request):
    return render(request, 'BookingRoomApp/sign_up.html')

def home(request):
    return render(request, 'BookingRoomApp/home.html')

def reservacion(request):
    tipos_servicio = TipoServicio.objects.filter(disposicion=True)
    return render(request, 'BookingRoomApp/reservacion.html', {'tipos_servicio': tipos_servicio})

def servicios(request):
    return render(request, 'BookingRoomApp/administracion/servicios.html')

def trabajadores(request):
    return render(request, 'BookingRoomApp/administracion/trabajadores.html')

def salones(request):
    return render(request, 'BookingRoomApp/administracion/salones.html')

def mobiliario(request):
    return render(request, 'BookingRoomApp/administracion/mobiliario.html')

def equipamiento(request):
    return render(request, 'BookingRoomApp/administracion/equipamiento.html')

def historial_reservacion(request):
    return render(request, 'BookingRoomApp/recepcion/historial_reservacion.html')

def inventario_equipamiento(request):
    return render(request, 'BookingRoomApp/almacen/inventario_equipamiento.html')

def inventario_mobiliario(request):
    return render(request, 'BookingRoomApp/almacen/inventario_mobiliario.html')

def pagos(request):
    return render(request, 'BookingRoomApp/recepcion/pagos.html')

def estadisticas(request):
    return render(request, 'BookingRoomApp/administracion/estadisticas.html')