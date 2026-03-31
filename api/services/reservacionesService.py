from decimal import Decimal

from django.db import transaction
from django.core.exceptions import ValidationError
from BookingRoomApp import models
from .montajeService import crear_montaje
from .herramientas import Precios

def crear_reseracion(datos):
    with transaction.atomic():
        equipos = datos.pop('reserva_equipa', [])
        servicios = datos.pop('reserva_servicio', [])
        mobiliarios = datos['montaje']['mobiliarios']

        localizador_precio = Precios(servicios=servicios, 
                                     salon=datos['montaje']['salon'], 
                                     mobiliarios=mobiliarios, equipamientos=equipos)
        
        montaje = crear_montaje(datos['montaje'])
        
        subtotal = localizador_precio.sumar_todo()
        IVA = subtotal * Decimal(0.16)
        total = subtotal + IVA

        reservacion = models.Reservacion.objects.create(nombre=datos['nombre'], descripEvento=datos['descripEvento'], 
                                                        estimaAsistentes=datos['estimaAsistentes'], fechaEvento=datos['fechaEvento'], 
                                                        horaInicio=datos['horaInicio'], horaFin=datos['horaFin'], 
                                                        subtotal=subtotal, IVA=IVA, total=total, 
                                                        cliente_id=datos['cliente'], montaje_id=montaje.pk, estado_reserva_id='PENDI', 
                                                        tipo_evento_id=datos['tipo_evento'], trabajador_id=datos['trabajador'])

        for servicio in servicios:
            reservacion.reserva_servicio.add(servicio['id'])

        for equipo in equipos:
            models.ReservaEquipa.objects.create(cantidad=equipo['cantidad'], reservacion_id=reservacion.pk, equipamiento_id=equipo['id'])

        models.RegistrEstadReserva.objects.create(reservacion_id=reservacion.pk, estado_reserva_id="PENDI")

        # la modificacion de estados de salon, equipamientos y mobiliarios se hacen cuando la reservacion sea aceptada (cuando este pagada)
        # en caso de cambiar el estado (desde el historial), se cambiaran los estados de equipamientos, mobiliarios y salon desde el service de cambio estao de reservacion

        return reservacion

def cambio_estado_reservacion(original, estado_nuevo):
    with transaction.atomic():
        # Se cambia el estado del salon
        texto_estado = estado_nuevo.pk
        original.estado_reserva_id = estado_nuevo
        original.save(update_fields=['estado_reserva'])
        # se crea un registro para determinar el dia en q se realizo el cambio de estado
        models.RegistrEstadReserva.objects.create(reservacion_id=original.pk, estado_reserva_id=texto_estado)

        # sei se trata de un pago, se registran los equipmaientos, mobiliarios y el salon guardanlos para la reservacion
        if texto_estado == 'PAGAD':
            #se guarda el salon y el registro de estados del salon
            montaje = models.Montaje.objects.get(id=original.montaje.pk)
            models.RegistrEstadSalon.objects.create(salon_id=montaje.salon.pk, estado_salon_id='RESER', fecha=original.fechaEvento)

            # se cambian los estados de los mobiliarios (esto por medio de su inventario)
            mobiliarios = models.MontajeMobiliario.objects.filter(montaje_id=montaje.pk)
            for mobiliario in mobiliarios:
                # por cada mobiliario del montaje, se obtiene el registro
                mobil = models.Mobiliario.objects.get(id=mobiliario.mobiliario.pk)
                #se cambia su estado
                estado = models.InventarioMob.objects.get(mobiliario_id=mobil.pk, estado_mobil_id='DISPO')
                # se modifica su cantidad en dicho estado
                estado.cantidad -= mobiliario.cantidad
                estado.save(update_fields=['cantidad'])
                # se crea o se obtiene el registro de reservado
                # si no existia se crae con cantidad igual a la de los equipamientso a utilizar
                inventario, fue_creado = models.InventarioMob.objects.get_or_create(
                    mobiliario_id= mobil.pk,
                    estado_mobil_id= 'RESER',
                    defaults= {
                        'cantidad': mobiliario.cantidad,
                    }
                )
                # si ya existia el registro se actualiza la cantidad, sumandole los nuevos equipamientos que pasan a dicho estado
                if not fue_creado:
                    inventario.cantidad += mobiliario.cantidad
                    inventario.save(update_fields=['cantidad'])

            # funciona exactamente igual que la logica para mobiliario pero para equipamientos
            equipos = models.ReservaEquipa.objects.filter(reservacion_id=original.pk)
            for equipo in equipos:
                equipamiento = models.Equipamiento.objects.get(id=equipo.equipamiento.pk)
                inventario = models.InventarioEquipa.objects.get(equipamiento_id=equipamiento.pk, estado_equipa_id='DISPO')
                inventario.cantidad -= equipo.cantidad
                inventario.save(update_fields=['cantidad'])
                inventarioequipa, fue_creado = models.InventarioEquipa.objects.get_or_create(
                    equipamiento_id= equipamiento.pk,
                    estado_equipa_id='RESER',
                    defaults={
                        'cantidad': equipo.cantidad
                    }
                )
                if not fue_creado:
                    inventarioequipa.cantidad += equipo.cantidad
                    inventarioequipa.save(update_fields=['cantidad'])

        # si se cancela una reservacion, es necesario modificar estados de mobilairios, equipamientos (inventarios), posterior se tienen que eliminar el registro de estado del salon, y actualizar registro de reservacion
        elif texto_estado == 'CANCE':
            montaje = models.Montaje.objects.get(id=original.montaje.pk)
            models.RegistrEstadSalon.objects.get(salon_id=montaje.salon.pk, estado_salon_id='RESER', fecha=original.fechaEvento).delete()

            # se obtienen los mobiliarios del montaje utilizado en la reservacion
            mobiliarios = models.MontajeMobiliario.objects.filter(montaje_id=montaje.pk)
            for mobiliario in mobiliarios:
                # se obtiene el mobiliario
                mobil = models.Mobiliario.objects.get(id=mobiliario.mobiliario.pk)

                # se obtienen los disponibles y se le suma la cantidad q era de la reservacion
                estado = models.InventarioMob.objects.get(mobiliario_id=mobil.pk, estado_mobil_id='DISPO')
                estado.cantidad += mobiliario.cantidad
                estado.save(update_fields=['cantidad'])

                # se obtienen los reservados y se le resta la cantidad q era de la reservacion
                inventario = models.InventarioMob.objects.get(mobiliario_id=mobil.pk, estado_mobil_id='RESER')
                inventario.cantidad -= mobiliario.cantidad
                inventario.save(update_fields=['cantidad'])

            # misma logica q arriba
            equipos = models.ReservaEquipa.objects.filter(reservacion_id=original.pk)
            for equipo in equipos:
                equipamiento = models.Equipamiento.objects.get(id=equipo.equipamiento.pk)

                estado = models.InventarioEquipa.objects.get(equipamiento_id=equipamiento.pk, estado_equipa_id='DISPO')
                estado.cantidad += equipo.cantidad
                estado.save(update_fields=['cantidad'])
                
                inventario = models.InventarioEquipa.objects.get(equipamiento_id=equipamiento.pk, estado_equipa_id='RESER')
                inventario.cantidad -= equipo.cantidad
                inventario.save(update_fields=['cantidad'])