from django.db import transaction
from django.core.exceptions import ValidationError
from BookingRoomApp import models
from .montajeService import crear_montaje
from .herramientas import Precios
from django.utils import timezone

from decimal import Decimal

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

        # en caso de no ingresarse el estado en el que se encontrara la reservacion, se pone automaticamente com pendiente
        if not datos.get('estado_reserva'):
            estado = 'PENDI'
        else:
            # en caso de que si haya un estado, se pondra el estado como tal
            estado = datos['estado_reserva']
            if datos['estado_reserva'] == "PAQUE":
                # en caso de que el estado sea paquete se pondra el subtotal ingresado desde el json
                subtotal = Decimal(datos["subtotal"])
 
        IVA = subtotal * Decimal(0.16)
        total = subtotal + IVA

        # seccion de validacion en contra de nulos en el envio
        if not datos.get('fechaEvento'):
            fechaEvento = None
        else:
            fechaEvento = datos['fechaEvento']

        if not datos.get('horaInicio'):
            horaInicio = None
        else:
            horaIncio = datos['horaInicio']

        if not datos.get('horaFin'):
            horaFin = None
        else:
            horaFin = datos['horaFin']

        if not datos.get('trabajador'):
            trabajdor = None
        else:
            trabajdor = datos['trabajador']
        
        if not datos.get('cliente'):
            cliente = None
        else:
            cliente = models.DatosCliente.objects.get(rfc=datos['cliente']).id

        if not datos.get('es_paquete'):
            es_paquete = False    
        else:
            es_paquete = datos['es_paquete']    

        reservacion = models.Reservacion.objects.create(nombreEvento=datos['nombre'], descripEvento=datos['descripEvento'], 
                                                        estimaAsistentes=datos['estimaAsistentes'], fechaEvento=fechaEvento, 
                                                        horaInicio=horaIncio, horaFin=horaFin, subtotal=subtotal, IVA=IVA, 
                                                        total=total, cliente_id=cliente, montaje_id=montaje.pk, estado_reserva_id=estado, 
                                                        tipo_evento_id=datos['tipo_evento'], trabajador_id=trabajdor, es_paquete= es_paquete)

        for servicio in servicios:
            models.ReservaServicio.objects.create(servicio_id=servicio['id'], reservacion_id=reservacion.id)

        for equipo in equipos:
            models.ReservaEquipa.objects.create(cantidad=equipo['cantidad'], reservacion_id=reservacion.pk, equipamiento_id=equipo['id'])

        if estado != "PAQUE":
            models.RegistrEstadReserva.objects.create(reservacion_id=reservacion.pk, estado_reserva_id=estado)

        # la modificacion de estados de salon, equipamientos y mobiliarios se hacen cuando la reservacion sea aceptada (cuando este pagada)
        # en caso de cambiar el estado (desde el historial), se cambiaran los estados de equipamientos, mobiliarios y salon desde el service de cambio estao de reservacion

        return reservacion


def cambio_estado_reservacion(original, estado_nuevo):
    with transaction.atomic():

        estado_anterior = original.estado_reserva_id

        # Se cambia el estado del salon
        texto_estado = estado_nuevo
        original.estado_reserva_id = texto_estado
        original.save(update_fields=['estado_reserva'])

        # se crea un registro para determinar el dia en q se realizo el cambio de estado
        models.RegistrEstadReserva.objects.create(reservacion_id=original.pk, estado_reserva_id=texto_estado)

        # sei se trata de un pago, se registran los equipmaientos, mobiliarios y el salon guardanlos para la reservacion
        if texto_estado in ['PAGAD', 'LIQUI', 'ENPRO'] and estado_anterior not in ['PAGAD', 'LIQUI', 'ENPRO']:

            #se guarda el salon y el registro de estados del salon
            montaje = models.Montaje.objects.get(id=original.montaje.pk)
            
            # para verficiar q el salon no este ocupado ese mismo dia
            control = models.RegistrEstadSalon.objects.filter(salon_id=montaje.salon_id, fecha=original.fechaEvento).exists()

            if control:
                raise Exception(f"El salon ya se encuentra ocupado ese dia, control: {control}")
            
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
        elif texto_estado == 'CANCE' and estado_anterior in ['ENPRO', 'PAGAD', 'LIQUI']:
            montaje = models.Montaje.objects.get(id=original.montaje.pk)
            models.RegistrEstadSalon.objects.filter(salon_id=montaje.salon_id, estado_salon_id='RESER', fecha=original.fechaEvento).delete()

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


def modificacion_aditamentos(original, nuevos_datos):
    with transaction.atomic():
        
        reservacion = models.Reservacion.objects.get(id=original.id)

        new_mobilairios = nuevos_datos.pop('mobiliarios', [])
        new_equipamientos = nuevos_datos.pop('reserva_equipa', [])
        new_servicios = nuevos_datos.pop('reserva_servicio', [])

        new_subtotal = nuevos_datos.pop('subtotal', None)

        # calculamos el total actual
        old_costo_elemtnso = Decimal('0.0')
        if reservacion.es_paquete:
            for mob in models.MontajeMobiliario.objects.filter(montaje_id=reservacion.montaje.id):
                old_costo_elemtnso += (Decimal(mob.mobiliario.costo) * Decimal(mob.cantidad))
            for equipo in models.ReservaEquipa.objects.filter(reservacion_id=reservacion.id):
                old_costo_elemtnso += (Decimal(equipo.equipamiento.costo) * Decimal(equipo.cantidad))
            for servicio in models.ReservaServicio.objects.filter(reservacion_id= reservacion.id):
                old_costo_elemtnso += servicio.servicio.costo


        for campo, valor in nuevos_datos.items():
            if campo == 'fechaEvento':
                montaje = models.Montaje.objects.get(id=reservacion.montaje.id)
                registro_salon = models.RegistrEstadSalon.objects.filter(salon_id=montaje.salon.id, fecha=reservacion.fechaEvento, estado_salon='RESER').first()
                
                if registro_salon:
                    registro_salon.fecha = valor
                    registro_salon.save(update_fields=['fecha'])

            if hasattr(reservacion, f"{campo}_id") and isinstance(valor, (str, int)):
                setattr(reservacion, f"{campo}_id", valor)
            else:
                setattr(reservacion, campo, valor)

        reservacion.save()

        estado = reservacion.estado_reserva.codigo

        if estado == 'ENPRO':
            _creacion_registros(reservacion, new_mobilairios, new_equipamientos, new_servicios)
        elif estado == 'FINAL':
            raise Exception("La reservacion ya ha sido finalizada, no se puede modificar")
        elif estado in ['LIQUI', 'PAGAD']:
            _modificacion_inventarios(reservacion, new_mobilairios, new_equipamientos, new_servicios)
        else:
            _modificacion_registros(reservacion, new_mobilairios, new_equipamientos, new_servicios)

        # si se envia el subtotal no se discute y se pone como subtotal
        if new_subtotal is not None:
            reservacion.subtotal = Decimal(new_subtotal)
            reservacion.IVA = reservacion.subtotal * Decimal('0.16')
            reservacion.total = reservacion.subtotal + reservacion.total
            reservacion.save(update_fields=['subtotal', 'IVA', 'total'])

        # si la reservacion no viene de un paquete, se recalcula todo
        elif not reservacion.es_paquete:
            new_subtotal_calculado = Decimal(reservacion.montaje.salon.costo)
            for mob in models.MontajeMobiliario.objects.filter(montaje_id=reservacion.montaje.id):
                new_subtotal_calculado += (Decimal(mob.mobiliario.costo) * Decimal(mob.cantidad))
            for equipo in models.ReservaEquipa.objects.filter(reservacion_id=reservacion.id):
                new_subtotal_calculado += (Decimal(equipo.equipamiento.costo) * Decimal(equipo.cantidad))
            for servicio in models.ReservaServicio.objects.filter(reservacion_id= reservacion.id):
                new_subtotal_calculado += servicio.servicio.costo
            reservacion.subtotal = new_subtotal_calculado
            reservacion.IVA = new_subtotal_calculado * Decimal('0.16')
            reservacion.total = new_subtotal_calculado + reservacion.IVA
            reservacion.save(update_fields=['subtotal', 'IVA', 'total'])
        
        # si la reservacion si es un paquete, solo se suman los nuevos anadidos, esto se hace restando el
        # total anterior al generado por el nuevo total
        else:
            new_costo_elemtnso = Decimal('0.0')
            for mob in models.MontajeMobiliario.objects.filter(montaje_id=reservacion.montaje.id):
                new_costo_elemtnso += (Decimal(mob.mobiliario.costo) * Decimal(mob.cantidad))
            for equipo in models.ReservaEquipa.objects.filter(reservacion_id=reservacion.id):
                new_costo_elemtnso += (Decimal(equipo.equipamiento.costo) * Decimal(equipo.cantidad))
            for servicio in models.ReservaServicio.objects.filter(reservacion_id= reservacion.id):
                new_costo_elemtnso += servicio.servicio.costo
            
            diferencia_csotos = new_costo_elemtnso - old_costo_elemtnso
            reservacion.subtotal = reservacion.subtotal + diferencia_csotos
            reservacion.IVA = reservacion.subtotal * Decimal('0.16')
            reservacion.total = reservacion.subtotal + reservacion.IVA
            reservacion.save(update_fields=['subtotal', 'IVA', 'total'])


# en este caso nada mas se hace modificacion de los registros intermedios, se ignoran inventarios
def _modificacion_registros(reservacion, new_mobilairios, new_equipamientos, new_servicios):
    with transaction.atomic():
        monta = reservacion.montaje.id
        if new_mobilairios is not None:
            ids_entrantes_mob = [mob['id'] for mob in new_mobilairios]
            models.MontajeMobiliario.objects.filter(montaje_id=monta).exclude(mobiliario_id__in=ids_entrantes_mob).delete()

            for mob in new_mobilairios:
                mobi, creado = models.MontajeMobiliario.objects.get_or_create(montaje_id=monta, mobiliario_id=mob['id'], defaults={'cantidad': mob['cantidad'], 'completado': False})

                if not (creado):
                    mobi.cantidad = mob['cantidad']
                    mobi.completado = False
                    mobi.save()
        
        if new_equipamientos is not None:
            ids_entrantes_equipos = [equipo['id'] for equipo in new_equipamientos]
            models.ReservaEquipa.objects.filter(reservacion_id=reservacion.id).exclude(equipamiento_id__in=ids_entrantes_equipos).delete()

            for equipo in new_equipamientos:
                equip, creado = models.ReservaEquipa.objects.get_or_create(reservacion_id=reservacion.id, equipamiento_id=equipo['id'], defaults={'cantidad': equipo['cantidad'], 'completado': False})

                if not (creado):
                    equip.cantidad = equipo['cantidad']
                    equip.completado = False
                    equip.save()

        if new_servicios is not None:
            ids_entrantes_servicios = [servicio['id'] for servicio in new_servicios]
            models.ReservaServicio.objects.filter(reservacion_id=reservacion.id).exclude(servicio_id__in=ids_entrantes_servicios).delete()

            for servicio in new_servicios:
                models.ReservaServicio.objects.get_or_create(reservacion_id=reservacion.id, servicio_id=servicio['id'])

# se guardan los objetos e inventarios puesto que se espera que ya este como minimo hecho un pago para la reservacion
def _modificacion_inventarios(reservacion, new_mobilairios, new_equipamientos, new_servicios):
    with transaction.atomic():
        monta = reservacion.montaje.id

        if new_mobilairios is not None:
            ids_entrantes_mob = [mob['id'] for mob in new_mobilairios]
            registros_eliminar = models.MontajeMobiliario.objects.filter(montaje_id=monta).exclude(mobiliario_id__in=ids_entrantes_mob)
            for mob in registros_eliminar:
                _liberar_reservados_mobiliarios(mob)
                mob.delete()

            for mob in new_mobilairios:
                mobi, creado = models.MontajeMobiliario.objects.get_or_create(montaje_id=monta, mobiliario_id=mob['id'], defaults={'cantidad': mob['cantidad'], 'completado': False})

                if not (creado):
                    _liberar_reservados_mobiliarios(mobi)
                    mobi.cantidad = mob['cantidad']
                    mobi.completado = False
                    mobi.save()

                _actualizar_inventario_mobiliario(mob)

        if new_equipamientos is not None:
            ids_entrantes_equipos = [equipo['id'] for equipo in new_equipamientos]
            equipos_eliminar = models.ReservaEquipa.objects.filter(reservacion_id=reservacion.id).exclude(equipamiento_id__in=ids_entrantes_equipos)
            
            for equipo in equipos_eliminar:
                _liberar_reservados_equipos(equipo)
                equipo.delete()

            for equipo in new_equipamientos:
                equip, creado = models.ReservaEquipa.objects.get_or_create(reservacion_id=reservacion.id, equipamiento_id=equipo['id'], defaults={'cantidad': equipo['cantidad'], 'completado': False})

                if not (creado):
                    _liberar_reservados_equipos(equip)
                    equip.cantidad = equipo['cantidad']
                    equip.completado = False
                    equip.save()

                _actualizar_inventario_equipos(equipo)
        
        if new_servicios is not None:
            ids_entrantes_servicios = [servicio['id'] for servicio in new_servicios]
            models.ReservaServicio.objects.filter(reservacion_id=reservacion.id).exclude(servicio_id__in=ids_entrantes_servicios).delete()

            for servicio in new_servicios:
                models.ReservaServicio.objects.get_or_create(reservacion_id=reservacion.id, servicio_id=servicio['id'])
            
# crea los registros desde cero para que se guarden como extras
def _creacion_registros(reservacion, new_mobiliarios, new_equipamientos, new_servicios):
    with transaction.atomic():
        monta = reservacion.montaje.id
        
        for mob in new_mobiliarios:
            inventario = models.InventarioMob.objects.get(mobiliario_id=mob['id'], estado_mobil='DISPO')
            if mob['cantidad'] > inventario.cantidad:
                raise Exception("No hay suficiente inventario disponible para este extra.")
            models.MontajeMobiliario.objects.create(montaje_id=monta, mobiliario_id=mob['id'], cantidad=mob['cantidad'], extra=True)
            _actualizar_inventario_mobiliario(mob)
            
        for equipo in new_equipamientos:
            inventario = models.InventarioEquipa.objects.get(equipamiento_id=equipo['id'], estado_equipa='DISPO')
            if equipo['cantidad'] > inventario.cantidad: 
                raise Exception("No hay suficiente inventario disponible para este extra.")
            models.ReservaEquipa.objects.create(reservacion_id=reservacion.id, equipamiento_id=equipo['id'], cantidad=equipo['cantidad'], extra=True)
            _actualizar_inventario_equipos(equipo)
            
        for servicio in new_servicios:
            models.ReservaServicio.objects.create(reservacion_id=reservacion.id, servicio_id=servicio['id'], extra=True)

# modifica inventarios cambiando cantidades de acuerdo a lo reservado, para equipamientos
def _actualizar_inventario_equipos(new_equipo):
    with transaction.atomic():

        inventario_dispo = models.InventarioEquipa.objects.get(equipamiento_id=new_equipo['id'], estado_equipa_id='DISPO')
        inventario_reser = models.InventarioEquipa.objects.get(equipamiento_id=new_equipo['id'], estado_equipa_id='RESER')

        inventario_dispo.cantidad -= new_equipo['cantidad']
        inventario_reser.cantidad += new_equipo['cantidad']

        inventario_dispo.save()
        inventario_reser.save()

# modifica inventarios cambiando cantidades de acuerdo a lo reservado, para mobiliarios
def _actualizar_inventario_mobiliario(new_mobiliario):
    with transaction.atomic():

        inventario_dispo = models.InventarioMob.objects.get(mobiliario_id=new_mobiliario['id'], estado_mobil_id='DISPO')
        inventario_reser = models.InventarioMob.objects.get(mobiliario_id=new_mobiliario['id'], estado_mobil_id='RESER')

        inventario_dispo.cantidad -= new_mobiliario['cantidad']
        inventario_reser.cantidad += new_mobiliario['cantidad']

        inventario_dispo.save()
        inventario_reser.save()

# funcion de apoyo para revertir cambios de estados en mobilairios
def _liberar_reservados_mobiliarios(old_mob):
    with transaction.atomic():
        inventario_di = models.InventarioMob.objects.get(estado_mobil='DISPO', mobiliario_id=old_mob.mobiliario)
        inventario_re = models.InventarioMob.objects.get(estado_mobil='RESER', mobiliario_id=old_mob.mobiliario)
        inventario_di.cantidad += old_mob.cantidad
        inventario_re.cantidad -= old_mob.cantidad
        inventario_di.save(update_fields=['cantidad'])
        inventario_re.save(update_fields=['cantidad'])


# funcion de apoyo para cambiar estados de equipamientos
def _liberar_reservados_equipos(old_equipo):
    with transaction.atomic():
        inventario_di = models.InventarioEquipa.objects.get(estado_equipa='DISPO', equipamiento_id=old_equipo.equipamiento)
        inventario_re = models.InventarioEquipa.objects.get(estado_equipa='RESER', equipamiento_id=old_equipo.equipamiento)
        inventario_di.cantidad += old_equipo.cantidad
        inventario_re.cantidad -= old_equipo.cantidad
        inventario_di.save(update_fields=['cantidad'])
        inventario_re.save(update_fields=['cantidad'])


def eliminar_reservacion(reserva):
    with transaction.atomic():
        reservacion = models.Reservacion.objects.get(id=reserva.id)

        montaje = reservacion.montaje
        montaje_mobiliario = models.MontajeMobiliario.objects.filter(montaje_id=montaje.id)
        servicios = models.ReservaServicio.objects.filter(reservacion_id=reservacion.id)
        equipos = models.ReservaEquipa.objects.filter(reservacion_id=reservacion.id)

        for montaje_mobiliari in montaje_mobiliario:
            montaje_mobiliari.delete()
        for servicio in servicios:
            servicio.delete()
        for equipo in equipos:
            equipo.delete()
        
        reservacion.delete()
        montaje.delete()

def obtener_reservacion_proxima(cliente_rfc):
    hoy = timezone.now().date()

    prosima = models.Reservacion.objects.filter(cliente__rfc=cliente_rfc, fechaEvento__gte=hoy, estado_reserva__codigo__in=['PAGAD', 'LIQUI', 'ENPRO']
                                                ).order_by('fechaEvento', 'horaInicio').first()
    
    if prosima:
        return prosima
    
    return None
