from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


def paquetes(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    paquetes = models.Reservacion.objects.filter(estado_reserva__codigo='PAQUE').select_related('montaje__salon', 'montaje__tipo_montaje', 'tipo_evento')
    paquetes_total = models.Reservacion.objects.filter(estado_reserva__codigo='PAQUE').count()
    salones = models.Salon.objects.all()
    tipos_montaje = models.TipoMontaje.objects.all()
    tipos_mobiliarios = models.TipoMobil.objects.filter(disposicion=True)
    tipos_servicio = models.TipoServicio.objects.filter(disposicion=True)
    tipos_equipamiento = models.TipoEquipa.objects.filter(disposicion=True)
    tipos_eventos = models.TipoEvento.objects.filter(disposicion=True)

    return render(request, "BookingRoomApp/administracion/paquetes.html", {
        'paquetes': paquetes,
        'paquetes_total': paquetes_total,
        "salones": salones,
        "tipos_montaje": tipos_montaje,
        "tipos_servicio": tipos_servicio,
        "tipos_equipamiento": tipos_equipamiento,
        "tipos_mobiliario": tipos_mobiliarios,
        "tipos_eventos": tipos_eventos,
        "rol": rol,
    })