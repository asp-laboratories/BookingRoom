from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from BookingRoomApp.views import get_cuenta_and_rol


def pagos(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "BookingRoomApp/recepcion/pagos.html", {"rol": rol})


def estadisticas(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "BookingRoomApp/administracion/estadisticas.html", {"rol": rol})


def historial_reservacion(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'BookingRoomApp/recepcion/historial_reservacion.html', {'rol': rol})