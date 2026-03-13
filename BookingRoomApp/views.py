from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'BookingRoomApp/login.html')

def sign_up(request):
    return render(request, 'BookingRoomApp/sign_up.html')

def home(request):
    return render(request, 'BookingRoomApp/home.html')

def reservacion(request):
    return render(request, 'BookingRoomApp/reservacion.html')

def servicios(request):
    return render(request, 'BookingRoomApp/administracion/servicios.html')

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