#!/usr/bin/env python
"""
Script para agregar RegistrEstadSalon a reservaciones que no tienen registro
Ejecutar con: python manage.py shell < agregar_registros_salon.py
"""
import os
import sys

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookingRoom_Django.settings')

import django
django.setup()

from BookingRoomApp import models

# Estados de reservación que deben tener registro de salon
ESTADOS_ACTIVOS = ['CONF', 'CON', 'PAGAD', 'PROC', 'ENPRO', 'PEN', 'SOLIC']

# Estado del salon a asignar
ESTADO_SALON_DEFAULT = 'RESV'

def agregar_registros_salon():
    print("\n=== Agregando registros de estado salon ===\n")

    # Obtener reservaciones con estado activo
    reservaciones = models.Reservacion.objects.filter(
        estado_reserva__codigo__in=ESTADOS_ACTIVOS,
        montaje__isnull=False,
        montaje__salon__isnull=False,
        fechaEvento__isnull=False
    ).select_related('montaje', 'montaje__salon', 'estado_reserva')

    print(f"Reservaciones con estado activo: {reservaciones.count()}\n")

    creados = 0
    ya_existen = 0
    errores = 0
    sin_montaje = 0

    for reservacion in reservaciones:
        salon = reservacion.montaje.salon
        fecha = reservacion.fechaEvento

        if not salon or not fecha:
            sin_montaje += 1
            continue

        # Verificar si ya existe registro para esta fecha y salon
        existente = models.RegistrEstadSalon.objects.filter(
            salon=salon,
            fecha=fecha
        ).first()

        if existente:
            ya_existen += 1
            print(f"  [YA EXISTE] Res #{reservacion.pk}: {salon.nombre} - {fecha} (estado: {existente.estado_salon.codigo})")
        else:
            # Crear nuevo registro
            try:
                models.RegistrEstadSalon.objects.create(
                    salon=salon,
                    fecha=fecha,
                    estado_salon_id=ESTADO_SALON_DEFAULT
                )
                creados += 1
                print(f"  [CREADO] Res #{reservacion.pk}: {salon.nombre} - {fecha}")
            except Exception as e:
                errores += 1
                print(f"  [ERROR] Res #{reservacion.pk}: {e}")

    print(f"\n=== Resultados ===")
    print(f"RegistrEstadSalon creados: {creados}")
    print(f"Ya existían: {ya_existen}")
    print(f"Errores: {errores}")
    print(f"Sin montaje/salon: {sin_montaje}")

    # Mostrar resumen de todas las reservaciones con su registro
    print(f"\n=== Registros de estado salon actuales ===")
    registros = models.RegistrEstadSalon.objects.all().order_by('fecha', 'salon__nombre')
    for reg in registros:
        print(f"  {reg.fecha} - {reg.salon.nombre}: {reg.estado_salon.codigo}")

if __name__ == '__main__':
    agregar_registros_salon()