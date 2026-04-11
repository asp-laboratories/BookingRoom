from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import transaction
from BookingRoomApp import models

try:
    import firebase_admin
    from firebase_admin import auth
    FIREBASE_ENABLED = True
except:
    FIREBASE_ENABLED = False


def get_user_rol(request):
    cuenta_id = request.session.get("cuenta_id")
    if not cuenta_id:
        return None
    try:
        trabajador = models.Trabajador.objects.select_related("rol").get(
            cuenta_id=cuenta_id
        )
        return trabajador.rol.codigo
    except:
        return None


def get_cuenta_and_rol(request):
    cuenta_id = request.session.get("cuenta_id")
    if not cuenta_id:
        return None, None
    try:
        cuenta = models.Cuenta.objects.get(id=cuenta_id)
        cuenta.id_trabajador = None
        try:
            trabajador = models.Trabajador.objects.select_related("rol").get(
                cuenta_id=cuenta_id
            )
            rol = trabajador.rol.codigo
            cuenta.id_trabajador = trabajador.pk
        except models.Trabajador.DoesNotExist:
            rol = None
        return cuenta, rol
    except:
        return None, None


def require_login(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("cuenta_id"):
            return HttpResponseRedirect(reverse("login"))
        return view_func(request, *args, **kwargs)
    return wrapper


from BookingRoomApp.views.auth import *
from BookingRoomApp.views.gestion_reservaciones import *
from BookingRoomApp.views.gestion_servicios import *
from BookingRoomApp.views.gestion_equipamiento import *
from BookingRoomApp.views.gestion_salones import *
from BookingRoomApp.views.gestion_mobiliario import *
from BookingRoomApp.views.administracion_trabajadores import *
from BookingRoomApp.views.administracion_pagos import *

from BookingRoomApp.views.gestion_mobiliario import mobiliario_caracteristicas
from BookingRoomApp.views.gestion_servicios import crear_tipo
from BookingRoomApp.views.gestion_paquetes import paquetes