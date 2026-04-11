from django.utils import timezone
from itertools import chain

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


def login(request):
    return render(request, "BookingRoomApp/auth/login.html")


def sign_up(request):
    return render(request, "BookingRoomApp/auth/sign_up.html")


def home(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    return render(
        request, "BookingRoomApp/recepcion/home.html", {"cuenta": cuenta, "rol": rol}
    )


class Home(generic.View):
    template_name = "BookingRoomApp/recepcion/home.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        hoy = timezone.now().date()

        recientes = models.Reservacion.objects.filter(fechaEvento__gte=hoy).exclude(estado_reserva__codigo__in=['PAQUE', 'SOLIC', 'FINAL']).order_by('fechaEvento').distinct()[:10]
        solicitudes = models.Reservacion.objects.filter(estado_reserva__codigo='SOLIC', fechaEvento__gte=hoy).order_by('fechaEvento').distinct()[:10]

        reservaciones = list(chain(recientes, solicitudes))

        return render(request, self.template_name, {
            "cuenta": cuenta,
            "rol": rol,
            "reservaciones": reservaciones,
        })