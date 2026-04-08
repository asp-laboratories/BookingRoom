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

        # Estados para solicitudes (pendientes)
        estados_solicitud = ['PEN', 'SOLIC']
        
        # Estados para confirmados
        estados_confirmados = ['CON', 'PAGAD', 'ENPRO', 'FIN']

        reservaciones_solicitudes = models.Reservacion.objects.select_related(
            "cliente", "estado_reserva", "montaje__salon"
        ).filter(
            estado_reserva__codigo__in=estados_solicitud
        ).order_by('-fechaEvento', '-id')[:20]

        reservaciones_confirmados = models.Reservacion.objects.select_related(
            "cliente", "estado_reserva", "montaje__salon"
        ).filter(
            estado_reserva__codigo__in=estados_confirmados
        ).order_by('fechaEvento', '-id')[:20]

        return render(request, self.template_name, {
            "cuenta": cuenta,
            "rol": rol,
            "reservaciones_solicitudes": reservaciones_solicitudes,
            "reservaciones_confirmados": reservaciones_confirmados,
        })