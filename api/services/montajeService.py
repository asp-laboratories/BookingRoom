from django.db import transaction
from django.core.exceptions import ValidationError
from BookingRoomApp import models
from . import herramientas


def crear_montaje(data):
    with transaction.atomic():
        mobiliarios = data['mobiliarios']
        localizar_precio = herramientas.Precios(salon=data['salon'], mobiliarios=mobiliarios)
        montaje = models.Montaje.objects.create(salon_id=data['salon'], tipo_montaje_id=data['tipo_montaje'], costo=localizar_precio.sumar_montaje())
        for mobiliario in mobiliarios:
            models.MontajeMobiliario.objects.create(mobiliario_id=mobiliario['id'], cantidad=mobiliario['cantidad'], montaje_id=montaje.id)
        return montaje