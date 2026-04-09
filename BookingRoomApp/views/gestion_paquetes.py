from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


def paquetes(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    salones = models.Salon.objects.all()
    tipos_montaje = models.TipoMontaje.objects.all()
    tipos_servicio = models.TipoServicio.objects.filter(disposicion=True)
    tipos_equipamiento = models.TipoEquipa.objects.filter(disposicion=True)
    tipos_mobiliarios = models.TipoMobil.objects.filter(disposicion=True)
    tipos_eventos = models.TipoEvento.objects.filter(disposicion=True)

    return render(request, "BookingRoomApp/administracion/paquetes.html", {
        "salones": salones,
        "tipos_montaje": tipos_montaje,
        "tipos_servicio": tipos_servicio,
        "tipos_equipamiento": tipos_equipamiento,
        "tipos_mobiliario": tipos_mobiliarios,
        "tipos_eventos": tipos_eventos,
        "rol": rol,
    })