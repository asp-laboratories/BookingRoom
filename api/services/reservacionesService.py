from django.db import transaction
from django.core.exceptions import ValidationError
from BookingRoomApp import models
from .montajeService import crear_montaje
from .herramientas import Precios
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

def crear_reseracion(datos, confirmar_inventario=True):
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

        if not datos.get('estado_reserva'):
            estado = 'PEN'
        else:
            estado = datos['estado_reserva']

        cliente = models.DatosCliente.objects.get(rfc=datos['cliente'])

        # Get trabajador if provided, otherwise None
        trabajador_id = datos.get('trabajador')
        if trabajador_id == '' or trabajador_id is None:
            trabajador_obj = None
        else:
            try:
                trabajador_obj = models.Trabajador.objects.get(no_empleado=trabajador_id)
            except models.Trabajador.DoesNotExist:
                trabajador_obj = None

        reservacion = models.Reservacion.objects.create(nombreEvento=datos['nombre'], descripEvento=datos['descripEvento'], 
                                                        estimaAsistentes=datos['estimaAsistentes'], fechaEvento=datos['fechaEvento'], 
                                                        horaInicio=datos['horaInicio'], horaFin=datos['horaFin'], 
                                                        subtotal=subtotal, IVA=IVA, total=total, 
                                                        cliente_id=cliente.id, montaje_id=montaje.pk, estado_reserva_id=estado, 
                                                        tipo_evento_id=datos['tipo_evento'], trabajador=trabajador_obj)

        for servicio in servicios:
            models.ReservaServicio.objects.create(servicio_id=servicio['id'], reservacion_id=reservacion.id)

        # Solo decrementar inventario si confirmar_inventario es True
        if confirmar_inventario:
            for equipo in equipos:
                models.ReservaEquipa.objects.create(cantidad=equipo['cantidad'], reservacion_id=reservacion.pk, equipamiento_id=equipo['id'])
                reservar_equipamiento(equipo['id'], equipo['cantidad'])

            for mobiliario in mobiliarios:
                reservar_mobiliario(mobiliario['id'], mobiliario['cantidad'])
        else:
            # Ajustar automaticamente al stock disponible y decrementar
            for equipo in equipos:
                inventario_equipa = models.InventarioEquipa.objects.filter(
                    equipamiento_id=equipo['id'], 
                    estado_equipa_id='DISP'
                ).first()
                
                cantidad_real = min(equipo['cantidad'], inventario_equipa.cantidad) if inventario_equipa else 0
                
                models.ReservaEquipa.objects.create(cantidad=cantidad_real, reservacion_id=reservacion.pk, equipamiento_id=equipo['id'])
                
                if cantidad_real > 0 and inventario_equipa:
                    reservar_equipamiento(equipo['id'], cantidad_real)

            for mobiliario in mobiliarios:
                inventario_mob = models.InventarioMob.objects.filter(
                    mobiliario_id=mobiliario['id'], 
                    estado_mobil_id='DISP'
                ).first()
                
                cantidad_real = min(mobiliario['cantidad'], inventario_mob.cantidad) if inventario_mob else 0
                
                if cantidad_real > 0 and inventario_mob:
                    reservar_mobiliario(mobiliario['id'], cantidad_real)

        models.RegistrEstadReserva.objects.create(reservacion_id=reservacion.pk, estado_reserva_id="PEN")

        return reservacion


def reservar_mobiliario(mobiliario_id, cantidad):
    inventario_disp = models.InventarioMob.objects.filter(
        mobiliario_id=mobiliario_id, 
        estado_mobil_id='DISP'
    ).first()
    
    mobiliario = models.Mobiliario.objects.get(id=mobiliario_id)
    stock_disponible = inventario_disp.cantidad if inventario_disp else 0
    
    if not inventario_disp or inventario_disp.cantidad < cantidad:
        raise ValidationError({
            'producto': mobiliario.nombre,
            'stock_disponible': stock_disponible,
            'mensaje': f"No hay suficiente stock disponible de {mobiliario.nombre}. Stock actual: {stock_disponible}"
        })
    
    inventario_disp.cantidad -= cantidad
    inventario_disp.save(update_fields=['cantidad'])
    
    inventario_resv, created = models.InventarioMob.objects.get_or_create(
        mobiliario_id=mobiliario_id,
        estado_mobil_id='OCUP',
        defaults={'cantidad': cantidad}
    )
    if not created:
        inventario_resv.cantidad += cantidad
        inventario_resv.save(update_fields=['cantidad'])


def reservar_equipamiento(equipamiento_id, cantidad):
    inventario_disp = models.InventarioEquipa.objects.filter(
        equipamiento_id=equipamiento_id, 
        estado_equipa_id='DISP'
    ).first()
    
    equipamiento = models.Equipamiento.objects.get(id=equipamiento_id)
    stock_disponible = inventario_disp.cantidad if inventario_disp else 0
    
    if not inventario_disp or inventario_disp.cantidad < cantidad:
        raise ValidationError({
            'producto': equipamiento.nombre,
            'stock_disponible': stock_disponible,
            'mensaje': f"No hay suficiente stock disponible de {equipamiento.nombre}. Stock actual: {stock_disponible}"
        })
    
    inventario_disp.cantidad -= cantidad
    inventario_disp.save(update_fields=['cantidad'])
    
    inventario_resv, created = models.InventarioEquipa.objects.get_or_create(
        equipamiento_id=equipamiento_id,
        estado_equipa_id='RESV',  # Usar RESV en lugar de OCUP
        defaults={'cantidad': cantidad}
    )
    if not created:
        inventario_resv.cantidad += cantidad
        inventario_resv.save(update_fields=['cantidad'])

def cambio_estado_reservacion(original, estado_nuevo):
    with transaction.atomic():

        # Se cambia el estado del salon
        texto_estado = estado_nuevo
        original.estado_reserva_id = texto_estado
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
            models.RegistrEstadSalon.objects.create(salon_id=montaje.salon_id, estado_salon_id='RESV', fecha=original.fechaEvento)

            # se cambian los estados de los mobiliarios (esto por medio de su inventario)
            mobiliarios = models.MontajeMobiliario.objects.filter(montaje_id=montaje.pk)
            for mobiliario in mobiliarios:

                # por cada mobiliario del montaje, se obtiene el registro
                mobil = models.Mobiliario.objects.get(id=mobiliario.mobiliario.pk)

                #se cambia su estado
                estado = models.InventarioMob.objects.get(mobiliario_id=mobil.pk, estado_mobil_id='DISP')

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
                    estado_mobil_id= 'RESV',
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
                inventario = models.InventarioEquipa.objects.get(equipamiento_id=equipamiento.pk, estado_equipa_id='DISP')
                if inventario.cantidad < equipo.cantidad:
                    raise Exception(f"No hay suficiente {equipamiento.nombre} para reservar")
                inventario.cantidad -= equipo.cantidad
                inventario.save(update_fields=['cantidad'])
                inventarioequipa, fue_creado = models.InventarioEquipa.objects.get_or_create(
                    equipamiento_id= equipamiento.pk,
                    estado_equipa_id='RESV',
                    defaults={
                        'cantidad': equipo.cantidad
                    }
                )
                if not fue_creado:
                    inventarioequipa.cantidad += equipo.cantidad
                    inventarioequipa.save(update_fields=['cantidad'])

        # si se cancela una reservacion, es necesario modificar estados de mobilairios, equipamientos (inventarios), posterior se tienen que eliminar el registro de estado del salon, y actualizar registro de reservacion
        elif texto_estado == 'CAN':
            montaje = models.Montaje.objects.get(id=original.montaje.pk)
            models.RegistrEstadSalon.objects.filter(salon_id=montaje.salon_id, estado_salon_id='RESV', fecha=original.fechaEvento).delete()

            # se obtienen los mobiliarios del montaje utilizado en la reservacion
            mobiliarios = models.MontajeMobiliario.objects.filter(montaje_id=montaje.pk)
            for mobiliario in mobiliarios:

                # se obtiene el mobiliario
                mobil = models.Mobiliario.objects.get(id=mobiliario.mobiliario.pk)

                # se obtienen los disponibles y se le suma la cantidad q era de la reservacion
                estado = models.InventarioMob.objects.get(mobiliario_id=mobil.pk, estado_mobil_id='DISP')
                estado.cantidad += mobiliario.cantidad
                estado.save(update_fields=['cantidad'])

                # se obtienen los reservados y se le resta la cantidad q era de la reservacion
                inventario = models.InventarioMob.objects.get(mobiliario_id=mobil.pk, estado_mobil_id='RESV')
                inventario.cantidad -= mobiliario.cantidad
                inventario.save(update_fields=['cantidad'])

            # misma logica q arriba
            equipos = models.ReservaEquipa.objects.filter(reservacion_id=original.pk)
            for equipo in equipos:
                equipamiento = models.Equipamiento.objects.get(id=equipo.equipamiento.pk)

                estado = models.InventarioEquipa.objects.get(equipamiento_id=equipamiento.pk, estado_equipa_id='DISP')
                estado.cantidad += equipo.cantidad
                estado.save(update_fields=['cantidad'])
                
                inventario = models.InventarioEquipa.objects.get(equipamiento_id=equipamiento.pk, estado_equipa_id='RESV')
                inventario.cantidad -= equipo.cantidad
                inventario.save(update_fields=['cantidad'])


            
# para los casos de abajo es obligatorio poner el total final al llamar a la api con estos campos, esto para determinar
# cuanto se va a ocupar, se busca evitar a toda costa el tener q ingresar numeros negativos
# ejemplo: la reservacion ya tinha 34 sillas, se modifico y ahora hay 30 sillas y 4 taburetes, lo que se envia es eso
# 30 sillas y 4 taburetes, no -4 sillas y 4 taburetes
def modificacion_aditamentos(original, nuevos_datos):
    with transaction.atomic():
        reservacion = models.Reservacion.objects.get(id=original.id)

        # foamrto "id", "cantidad" (donde aplique)
        new_mobilairios = nuevos_datos.pop('mobiliarios', None)
        new_equipamientos = nuevos_datos.pop('reserva_equipa', None)
        new_servicios = nuevos_datos.pop('reserva_servicio', None)

        # se guardan demas campos de reservacion
        for campo, valor in nuevos_datos.items():
            
            # en caso de que se actualice la fecha del evento imporante actualizar el registro de ocupacion del salon
            if campo == 'fechaEvento':
                montaje = models.Montaje.objects.get(id=reservacion.montaje.id)
                registro_salon = models.RegistrEstadSalon.objects.get(salon_id=montaje.salon.id, fecha=reservacion.fechaEvento, estado_salon='RESV')
                registro_salon.fecha = valor
                registro_salon.save(update_fields=['fecha'])
            setattr(original, campo, valor)
        
        # se guardan los cambios
        original.save()
        
        costo_extra_total = 0
        
        # encaso de que se hayan agregado 
        if new_mobilairios:

            # obtenemos el montaje para poder guardar los cambios
            montaje = models.Montaje.objects.get(id=reservacion.montaje.id)

            # en caso de q la reservacion ya este en proceso debemos hacer registros nuevos en montaje mobiliario, esto justamente pq 
            # se tienen que tomar aparte estos aditamentos
            if reservacion.estado_reserva == 'ENPRO':

                # obtenemos los nuevos mobiliarios
                for new_mobil in new_mobilairios:
                    
                    # obtenemos su inventario disponible
                    inventario = models.InventarioMob.objects.get(mobiliario_id=new_mobil['id'], estado_mobil='DISP')

                    # validacion de que hay mas inventario disponible que cantidad pedida para la reservacion                    
                    if new_mobil['cantidad'] > inventario.cantidad:
                        raise Exception(f"No hay suficientes {new_mobil['id']} para la reservacion")
                    
                    # se ajustan registros de de disponibles y reservados
                    inventario.cantidad -= new_mobil['cantidad']
                    inventario.save(update_fields=['cantidad'])
                    inventario_2, fue_creado = models.InventarioMob.objects.get_or_create(
                        mobiliario_id=new_mobil['id'], 
                        estado_mobil='RESV',
                        defaults={
                            'cantidad': new_mobil['cantidad']
                        })
                    if not fue_creado:
                        inventario_2.cantidad += new_mobil['cantidad']
                        inventario_2.save(update_fields=['cantidad'])

                    # obtener costo del mobiliario
                    try:
                        mobil = models.Mobiliario.objects.get(id=new_mobil['id'])
                        costo_extra_total += float(mobil.costo) * new_mobil['cantidad']
                    except:
                        pass
                    
                    # se crean nuevos registro de asignacion de aditamentos extras
                    models.MontajeMobiliario.objects.create(montaje_id=montaje.id, mobiliario_id= new_mobil['id'], cantidad=new_mobil['cantidad'], extra=True)

            # en caso de que la reservacion este como pendiente, cancelada, solicitud se hace un caso especial para que no se
            # guaden las reservas de mobilairios
            elif reservacion.estado_reserva in ['CAN', 'PEN', 'SOLIC', 'CON']:
                for new_mobil in new_mobilairios:

                    # se intenta crear o obtener el registro de montaje mobiliario
                    montaje_mobil, fue_creado = models.MontajeMobiliario.objects.get_or_create(
                        mobiliario_id=new_mobil['id'], 
                        montaje_id= reservacion.montaje.id,
                        defaults= {
                            'cantidad': new_mobil['cantidad'],
                            'extra': True,  # Marcar como extra
                        })
                    
                    total = 0
                    if not fue_creado:                
                        total = montagem_mobil.cantidad
                        montagem_mobil.cantidad = new_mobil['cantidad']
                        montagem_mobil.completado = False
                        montaje_mobil.extra = True  # Asegurar que sea extra
                        montagem_mobil.save(update_fields=['cantidad', 'completado', 'extra'])
                    
                    # obtener costo del mobiliario
                    try:
                        mobil = models.Mobiliario.objects.get(id=new_mobil['id'])
                        costo_extra_total += float(mobil.costo) * new_mobil['cantidad']
                    except:
                        pass

                    # se obtiene el mobiliario disponible del mobiliario en iteracion
                    inventario = models.InventarioMob.objects.get(mobiliario_id=new_mobil['id'], estado_mobil='DISP')
                    if new_mobil['cantidad'] > (inventario.cantidad + total):
                        raise Exception(f"No hay suficientes {new_mobil['id']} para la reservacion")

            # en caso de q la reservacion aun no se este llevando a cabo pues nomas se hacen modificaciones de registros 
            else:

                for new_mobil in new_mobilairios:
                    
                    # si se obtiene, si es old, sino es new
                    old_mobil, creado = models.MontajeMobiliario.objects.get_or_create(
                        montaje_id=reservacion.montaje.id, 
                        mobiliario_id=new_mobil['id'], 
                        defaults={
                            'cantidad': new_mobil['cantidad'],
                            'extra': True,  # Marcar como extra
                        }
                    )

                    # si si es old se manda a liberar espacio, si no lo es se salta al siguiente paso
                    if not creado:
                        _liberar_reservados_mobiliarios(old_mobil)
                        old_mobil.cantidad = new_mobil['cantidad']
                        old_mobil.completado = False
                        old_mobil.extra = True  # Asegurar que sea extra
                        old_mobil.save(update_fields=['cantidad', 'completado', 'extra'])

                    # obtener costo del mobiliario
                    try:
                        mobil = models.Mobiliario.objects.get(id=new_mobil['id'])
                        costo_extra_total += float(mobil.costo) * new_mobil['cantidad']
                    except:
                        pass

                    # obtenemos disponibles del mobiliario actual (crear si no existe)
                    try:
                        inventario_di = models.InventarioMob.objects.get(mobiliario_id=new_mobil['id'], estado_mobil_id='DISP')
                    except models.InventarioMob.DoesNotExist:
                        # Crear inventario disponible si no existe
                        inventario_di = models.InventarioMob.objects.create(
                            mobiliario_id=new_mobil['id'],
                            estado_mobil_id='DISP',
                            cantidad=0
                        )
                    
                    try:
                        inventario_re, _ = models.InventarioMob.objects.get_or_create(
                            mobiliario_id=new_mobil['id'], 
                            estado_mobil_id='RESV',
                            defaults={'cantidad': 0}
                        )
                    except models.InventarioMob.DoesNotExist:
                        inventario_re = None

                    if new_mobil['cantidad'] > inventario_di.cantidad:
                        raise Exception(f"No hay suficientes {new_mobil['id']} para la reservacion")
                    
                    inventario_di.cantidad -= new_mobil['cantidad']
                    inventario_di.save(update_fields=['cantidad'])
                    
                    if inventario_re:
                        inventario_re.cantidad += new_mobil['cantidad']
                        inventario_re.save(update_fields=['cantidad'])


        # misma logica de funcionamiento que mobiliarios
        if new_equipamientos:
            if reservacion.estado_reserva == 'ENPRO':
                for new_equipo in new_equipamientos:
                    inventario = models.InventarioEquipa.objects.get(equipamiento_id=new_equipo['id'], estado_equipa='DISP')                 
                    if new_equipo['cantidad'] > inventario.cantidad:
                        raise Exception(f"No hay suficientes {new_equipo['id']} para la reservacion")
                    inventario.cantidad -= new_equipo['cantidad']
                    inventario.save(update_fields=['cantidad'])
                    inventario_2, fue_creado = models.InventarioEquipa.objects.get_or_create(
                        equipamiento_id=new_equipo['id'], 
                        estado_equipa='RESV',
                        defaults={
                            'cantidad': new_equipo['cantidad']
                        })
                    if not fue_creado:
                        inventario_2.cantidad += new_equipo['cantidad']
                        inventario_2.save(update_fields=['cantidad'])
                    
                    # obtener costo del equipamento
                    try:
                        equipo = models.Equipamiento.objects.get(id=new_equipo['id'])
                        costo_extra_total += float(equipo.costo) * new_equipo['cantidad']
                    except:
                        pass
                    
                    models.ReservaEquipa.objects.create(reservacion_id=reservacion.id, equipamiento_id=new_equipo['id'], cantidad= new_equipo['cantidad'], extra=True)

            elif reservacion.estado_reserva in ['CAN', 'PEN', 'SOLIC', 'PLANT', 'CON']:
                for new_equipo in new_equipamientos:
                    equipos_reserva, fue_creado = models.ReservaEquipa.objects.get_or_create(
                        equipamiento_id=new_equipo['id'], 
                        reservacion_id= reservacion.id,
                        defaults= {
                            'cantidad': new_equipo['cantidad'],
                            'extra': True,  # Marcar como extra
                        })
                    total = 0
                    if not fue_creado:
                        total = equipos_reserva.cantidad
                        equipos_reserva.cantidad = new_equipo['cantidad']
                        equipos_reserva.completado = False
                        equipos_reserva.extra = True  # Asegurar que sea extra
                        equipos_reserva.save(update_fields=['cantidad', 'completado', 'extra'])

                    # obtener costo del equipamento
                    try:
                        equipo = models.Equipamiento.objects.get(id=new_equipo['id'])
                        costo_extra_total += float(equipo.costo) * new_equipo['cantidad']
                    except:
                        pass

                    inventario = models.InventarioEquipa.objects.get(equipamiento_id=new_equipo['id'], estado_equipa='DISP')           
                    if new_equipo['cantidad'] > (inventario.cantidad + total):
                        raise Exception(f"No hay suficientes {new_equipo['id']} para la reservacion")

            else:
                for new_equipo in new_equipamientos:

                    old_equipo, creado = models.ReservaEquipa.objects.get_or_create(
                        reservacion_id=reservacion.id, 
                        equipamiento_id=new_equipo['id'], 
                        defaults={
                            'cantidad': new_equipo['cantidad'],
                            'extra': True,  # Marcar como extra
                        }
                    )

                    # si si es old se manda a liberar espacio, si no lo es se salta al siguiente paso
                    if not creado:
                        _liberar_reservados_equipos(old_equipo)
                        old_equipo.cantidad = new_equipo['cantidad']
                        old_equipo.completado = False
                        old_equipo.extra = True  # Asegurar que sea extra
                        old_equipo.save(update_fields=['cantidad', 'completado', 'extra'])

                    # obtener costo del equipamento
                    try:
                        equipo = models.Equipamiento.objects.get(id=new_equipo['id'])
                        costo_extra_total += float(equipo.costo) * new_equipo['cantidad']
                    except:
                        pass

                    # obtenemos disponibles del equipamento actual
                    try:
                        inventario_di = models.InventarioEquipa.objects.get(equipamiento_id=new_equipo['id'], estado_equipa_id='DISP')
                    except models.InventarioEquipa.DoesNotExist:
                        # Crear inventario disponible si no existe
                        inventario_di = models.InventarioEquipa.objects.create(
                            equipamiento_id=new_equipo['id'],
                            estado_equipa_id='DISP',
                            cantidad=0
                        )
                    
                    try:
                        inventario_re, _ = models.InventarioEquipa.objects.get_or_create(
                            equipamiento_id=new_equipo['id'], 
                            estado_equipa_id='RESV',
                            defaults={'cantidad': 0}
                        )
                    except models.InventarioEquipa.DoesNotExist:
                        inventario_re = None

                    if new_equipo['cantidad'] > inventario_di.cantidad:
                        raise Exception(f"No hay suficientes {new_equipo['id']} para la reservacion")
                    
                    inventario_di.cantidad -= new_equipo['cantidad']
                    inventario_di.save(update_fields=['cantidad'])
                    
                    if inventario_re:
                        inventario_re.cantidad += new_equipo['cantidad']
                        inventario_re.save(update_fields=['cantidad'])

        # logica parecido para anadir servicios
        if new_servicios:
            for servicio in new_servicios:
                # Obtener el costo del servicio
                try:
                    servicio_obj = models.Servicio.objects.get(id=servicio['id'])
                    costo_extra_total += float(servicio_obj.costo)
                except models.Servicio.DoesNotExist:
                    pass
                
                models.ReservaServicio.objects.create(
                    servicio_id=servicio['id'], 
                    reservacion_id=reservacion.id,
                    extra=True
                )
        
        # Actualizar precio total si hay costos extras
        if costo_extra_total > 0:
            reservacion.subtotal += Decimal(costo_extra_total)
            reservacion.IVA = reservacion.subtotal * Decimal(0.16)
            reservacion.total = reservacion.subtotal + reservacion.IVA
            reservacion.save(update_fields=['subtotal', 'IVA', 'total'])
            logger.info(f"Precio actualizado: reservacion {reservacion.id}, extra={costo_extra_total}, total={reservacion.total}")


# funcion de apoyo para revertir cambios de estados en mobilairios
def _liberar_reservados_mobiliarios(old_mob):
    try:
        inventario_di = models.InventarioMob.objects.get(estado_mobil='DISP', mobiliario_id=old_mob.mobiliario)
    except models.InventarioMob.DoesNotExist:
        inventario_di = None
    
    try:
        inventario_re = models.InventarioMob.objects.get(estado_mobil='RESV', mobiliario_id=old_mob.mobiliario)
    except models.InventarioMob.DoesNotExist:
        inventario_re = None
    
    if inventario_di:
        inventario_di.cantidad += old_mob.cantidad
        inventario_di.save(update_fields=['cantidad'])
    
    if inventario_re:
        inventario_re.cantidad -= old_mob.cantidad
        inventario_re.save(update_fields=['cantidad'])


# funcion de apoyo para cambiar estados de equipamientos
def _liberar_reservados_equipos(old_equipo):
    try:
        inventario_di = models.InventarioEquipa.objects.get(estado_equipa='DISP', equipamiento_id=old_equipo.equipamiento)
    except models.InventarioEquipa.DoesNotExist:
        inventario_di = None
    
    try:
        inventario_re = models.InventarioEquipa.objects.get(estado_equipa='RESV', equipamiento_id=old_equipo.equipamiento)
    except models.InventarioEquipa.DoesNotExist:
        inventario_re = None
    
    if inventario_di:
        inventario_di.cantidad += old_equipo.cantidad
        inventario_di.save(update_fields=['cantidad'])
    
    if inventario_re:
        inventario_re.cantidad -= old_equipo.cantidad
        inventario_re.save(update_fields=['cantidad'])