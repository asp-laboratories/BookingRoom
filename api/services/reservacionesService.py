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
        IVA = subtotal * 0.16
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

            # para verficiar q el salon no este ocupado ese mismo dia
            control = models.RegistrEstadSalon.objects.filter(salon_id=montaje.salon_id, fecha=original.fechaEvento).exists()
            if control:
                raise Exception("El salon ya se encuentra ocupado ese dia")
            models.RegistrEstadSalon.objects.create(salon_id=montaje.salon_id, estado_salon_id='RESER', fecha=original.fechaEvento)

            # se cambian los estados de los mobiliarios (esto por medio de su inventario)
            mobiliarios = models.MontajeMobiliario.objects.filter(montaje_id=montaje.pk)
            for mobiliario in mobiliarios:

                # por cada mobiliario del montaje, se obtiene el registro
                mobil = models.Mobiliario.objects.get(id=mobiliario.mobiliario.pk)

                #se cambia su estado
                estado = models.InventarioMob.objects.get(mobiliario_id=mobil.pk, estado_mobil_id='DISPO')

                # validacion para determinar que se pueden reservar los mobiliarios
                if estado.cantidad < mobiliario.cantidad:
                    raise Exception(f"No hay {mobil.nombre} para reservar")

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
                if inventario.cantidad < equipo.cantidad:
                    raise Exception(f"No hay suficiente {equipamiento.nombre} para reservar")
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
            models.RegistrEstadSalon.objects.get(salon_id=montaje.salon_id, estado_salon_id='RESER', fecha=original.fechaEvento).delete()

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


            
# para los casos de abajo es obligatorio poner el total final al llamar a la api con estos campos, esto para determinar
# cuanto se va a ocupar, se busca evitar a toda costa el tener q ingresar numeros negativos
# ejemplo: la reservacion ya tenia 34 sillas, se modifico y ahora hay 30 sillas y 4 taburetes, lo que se envia es eso
# 30 sillas y 4 taburetes, no -4 sillas y 4 taburetes
def modificacion_aditamentos(original, nuevos_datos):
    with transaction.atomic():
        reservacion = models.Reservacion.objects.get(id=original.id)

        # se guardan demas campos de reservacion
        for campo, valor in nuevos_datos.items():
            
            # en caso de que se actualice la fecha del evento imporante actualizar el registro de ocupacion del salon
            if campo == 'fechaEvento':
                montaje = models.Montaje.objects.get(id=reservacion.montaje.id)
                registro_salon = models.RegistrEstadSalon.objects.get(salon_id=montaje.salon.id, fecha=valor, estado_salon='RESER')
                registro_salon.fecha = valor
                registro_salon.save(update_fields=['fecha'])
            setattr(original, campo, valor)
        
        # se guardan los cambios
        original.save()

        # foamrto "id", "cantidad" (donde aplique)
        new_mobilairios = nuevos_datos.pop('mobiliarios', None)
        new_equipamientos = nuevos_datos.pop('reserva_equipa', None)
        new_servicios = nuevos_datos.pop('reserva_servicio', None)

        # encaso de que se hayan agregado 
        if new_mobilairios:

            # obtenemos el montaje para poder guardar los cambios
            montaje = models.Montaje.objects.get(id=reservacion.montaje.id)

            # en caso de q la reservacion ya este en proceso debemos hacer registros nuevos en montaje mobiliario, esto justamente pq 
            # se tienen que tomar aparte estos aditamentos
            if reservacion.estado_reserva.id == 'ENPRO':

                # obtenemos los nuevos mobiliarios
                for new_mobil in new_mobilairios:
                    
                    # obtenemos su inventario disponible
                    inventario = models.InventarioMob.objects.get(mobiliario_id=new_mobil['id'], estado_mobil='DISPO')

                    # validacion de que hay mas inventario disponible que cantidad pedida para la reservacion                    
                    if new_mobil['cantidad'] > inventario.cantidad:
                        raise Exception(f"No hay suficientes {new_mobil['id']} para la reservacion")
                    
                    # se ajustan registros de de disponibles y reservados
                    inventario.cantidad -= new_mobil['cantidad']
                    inventario.save(update_fields=['cantidad'])
                    inventario_2, fue_creado = models.InventarioMob.objects.get_or_create(
                        mobiliario_id=new_mobil['id'], 
                        estado_mobil='RESER',
                        defaults={
                            'cantidad': new_mobil['cantidad']
                        })
                    if not fue_creado:
                        inventario_2.cantidad += new_mobil['cantidad']
                        inventario_2.save(update_fields=['cantidad'])

                    # se crean nuevos registro de asignacion de aditamentos extras
                    models.MontajeMobiliario.objects.create(montaje_id=montaje.id, mobiliario_id= new_mobil['id'], cantidad=new_mobil['cantidad'])

            # en caso de que la reservacion este como pendiente, cancelada, solicitud se hace un caso especial para que no se
            # guaden las reservas de mobilairios
            elif reservacion.estado_reserva.id in ['CANCE', 'PENDI', 'SOLIC']:
                for new_mobil in new_mobilairios:

                    # se intenta crear o obtener el registro de montaje mobiliario, en caso de que se cree se dara en cantidad en
                    # cantidad el valor nuevo
                    montaje_mobil, fue_creado = models.MontajeMobiliario.objects.get_or_create(
                        mobiliario_id=new_mobil['id'], 
                        montaje_id= reservacion.montaje.id,
                        defaults= {
                            'cantidad': new_mobil['cantidad'],
                        })
                    
                    # si fue obtenido (ya existia), se establece la nueva cantidad del mobiliario necesitado
                    total = 0
                    if not fue_creado:                
                        total = montaje_mobil.cantidad
                        montaje_mobil.cantidad = new_mobil['cantidad']
                        montaje_mobil.completado = False
                        montaje_mobil.save(update_fields=['cantidad', 'completado'])
                    
                    # se obtiene el mobiliario disponible del mobiliario en iteracion
                    inventario = models.InventarioMob.objects.get(mobiliario_id=new_mobil['id'], estado_mobil='DISPO')
                    if new_mobil['cantidad'] > (inventario.cantidad + total):
                        raise Exception(f"No hay suficientes {new_mobil['id']} para la reservacion")

            # en caso de q la reservacion aun no se este llevando a cabo pues nomas se hacen modificaciones de registros 
            else:

                for new_mobil in new_mobilairios:

                    inventario_2, fue_creado = models.InventarioMob.objects.get_or_create(
                        mobiliario_id=new_mobil['id'], 
                        estado_mobil='RESER',
                        defaults={
                            'cantidad': new_mobil['cantidad']
                        })
                    if not fue_creado:
                        inventario_2.cantidad += new_mobil['cantidad']
                        inventario_2.save(update_fields=['cantidad'])

                    montaje_mobil, fue_creado = models.MontajeMobiliario.objects.get_or_create(
                        mobiliario_id=new_mobil['id'], 
                        montaje_id= reservacion.montaje.id,
                        defaults= {
                            'cantidad': new_mobil['cantidad'],
                        })
                    
                    total = 0
                    if not fue_creado:
                        total = montaje_mobil.cantidad
                        montaje_mobil.cantidad = new_mobil['cantidad']
                        montaje_mobil.completado = False
                        montaje_mobil.save(update_fields=['cantidad', 'completado'])
        
                    inventario = models.InventarioMob.objects.get(mobiliario_id=new_mobil['id'], estado_mobil='DISPO')
                    if new_mobil['cantidad'] > (inventario.cantidad + total):
                        raise Exception(f"No hay suficientes {new_mobil['id']} para la reservacion")            
                    inventario.cantidad -= new_mobil['cantidad']
                    inventario.save(update_fields=['cantidad'])

        # misma logica de funcionamiento que mobiliarios
        if new_equipamientos:
            if reservacion.estado_reserva.id == 'ENPRO':
                for new_equipo in new_equipamientos:
                    inventario = models.InventarioEquipa.objects.get(equipamiento_id=new_equipo['id'], estado_equipa='DISPO')                 
                    if new_equipo['cantidad'] > inventario.cantidad:
                        raise Exception(f"No hay suficientes {new_equipo['id']} para la reservacion")
                    inventario.cantidad -= new_equipo['cantidad']
                    inventario.save(update_fields=['cantidad'])
                    inventario_2, fue_creado = models.InventarioEquipa.objects.get_or_create(
                        equipamiento_id=new_equipo['id'], 
                        estado_equipa='RESER',
                        defaults={
                            'cantidad': new_equipo['cantidad']
                        })
                    if not fue_creado:
                        inventario_2.cantidad += new_equipo['cantidad']
                        inventario_2.save(update_fields=['cantidad'])
                    models.ReservaEquipa.objects.create(reservacion_id=reservacion.id, equipamiento_id=new_equipo['id'], cantidad= new_equipo['cantidad'])

            elif reservacion.estado_reserva.id in ['CANCE', 'PENDI', 'SOLIC']:
                for new_equipo in new_equipamientos:
                    equipos_reserva, fue_creado = models.ReservaEquipa.objects.get_or_create(
                        equipamiento_id=new_equipo['id'], 
                        reservacion_id= reservacion.id,
                        defaults= {
                            'cantidad': new_equipo['cantidad'],
                        })
                    total = 0
                    if not fue_creado:
                        total = equipos_reserva.cantidad
                        equipos_reserva.cantidad = new_equipo['cantidad']
                        equipos_reserva.completado = False
                        equipos_reserva.save(update_fields=['cantidad', 'completado'])

                    inventario = models.InventarioEquipa.objects.get(equipamiento_id=new_equipo['id'], estado_equipa='DISPO')           
                    if new_equipo['cantidad'] > (inventario.cantidad + total):
                        raise Exception(f"No hay suficientes {new_equipo['id']} para la reservacion")

            else:
                for new_equipo in new_equipamientos:
                    inventario_2, fue_creado = models.InventarioEquipa.objects.get_or_create(
                        equipamiento_id=new_equipo['id'], 
                        estado_equipa='RESER',
                        defaults={
                            'cantidad': new_equipo['cantidad']
                        })
                    if not fue_creado:
                        inventario_2.cantidad += new_equipo['cantidad']
                        inventario_2.save(update_fields=['cantidad'])
                    equipos_reserva, fue_creado = models.ReservaEquipa.objects.get_or_create(
                        equipamiento_id=new_equipo['id'], 
                        reservacion_id= reservacion.id,
                        defaults= {
                            'cantidad': new_equipo['cantidad'],
                        })
                    total = 0
                    if not fue_creado:
                        total = equipos_reserva.cantidad
                        equipos_reserva.cantidad = new_equipo['cantidad']
                        equipos_reserva.completado = False
                        equipos_reserva.save(update_fields=['cantidad', 'completado'])

                    inventario = models.InventarioEquipa.objects.get(equipamiento_id=new_equipo['id'], estado_equipa='DISPO')                 
                    if new_equipo['cantidad'] > (inventario.cantidad + total):
                        raise Exception(f"No hay suficientes {new_equipo['id']} para la reservacion")
                    inventario.cantidad -= new_equipo['cantidad']
                    inventario.save(update_fields=['cantidad'])

        # logica parecida para anadir servicios
        if new_servicios:
            for servicio in new_servicios:
                control = reservacion.reserva_servicio.filter(id=servicio['id']).exists()
                if control:
                    raise Exception(f"La reservacion ya tiene el servicio {servicio['id']}")
                else:
                    reservacion.reserva_servicio.add(servicio['id'])