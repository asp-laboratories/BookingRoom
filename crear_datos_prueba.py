import os
import sys
import django
from datetime import date, time, timedelta
from decimal import Decimal

sys.path.insert(0, '/home/luisdgr/Descargas/BookingRoom')
sys.path.insert(0, '/home/luisdgr/Descargas/BookingRoom/BookingRoom_Django')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from BookingRoomApp.models import (
    TipoCliente, Cuenta, DatosCliente, EstadoCuenta, 
    TipoEvento, EstadoReserva, Salon, TipoMontaje, Montaje,
    TipoServicio, Servicio, Reservacion, EstadoSalon
)

def crear_datos_prueba():
    # Crear tipos de cliente
    tipo_fisica, _ = TipoCliente.objects.get_or_create(codigo='FIS', defaults={'nombre': 'Persona Física', 'disposicion': True})
    tipo_moral, _ = TipoCliente.objects.get_or_create(codigo='MOR', defaults={'nombre': 'Persona Moral', 'disposicion': True})

    # Crear estado de cuenta
    estado_act, _ = EstadoCuenta.objects.get_or_create(codigo='ACT', defaults={'nombre': 'Activa'})

    # Crear cuentas y clientes
    clientes_data = [
        {'rfc': 'XAXX010101000', 'nombre_fiscal': 'Juan Pérez García', 'nombre': 'Juan', 'apellidoPaterno': 'Pérez', 'apelidoMaterno': 'García', 'telefono': '5551234567', 'email': 'juan.perez@email.com'},
        {'rfc': 'XAXX010102000', 'nombre_fiscal': 'María López Hernández', 'nombre': 'María', 'apellidoPaterno': 'López', 'apelidoMaterno': 'Hernández', 'telefono': '5552345678', 'email': 'maria.lopez@email.com'},
        {'rfc': 'XAXX010103000', 'nombre_fiscal': 'Carlos Ramírez Sánchez', 'nombre': 'Carlos', 'apellidoPaterno': 'Ramírez', 'apelidoMaterno': 'Sánchez', 'telefono': '5553456789', 'email': 'carlos.ramirez@email.com'},
    ]

    clientes = []
    for i, data in enumerate(clientes_data):
        cuenta, _ = Cuenta.objects.get_or_create(
            correo_electronico=data['email'],
            defaults={'nombre_usuario': data['nombre'], 'estado_cuenta': estado_act}
        )
        cliente, created = DatosCliente.objects.get_or_create(
            correo_electronico=data['email'],
            defaults={
                'rfc': data['rfc'],
                'nombre_fiscal': data['nombre_fiscal'],
                'nombre': data['nombre'],
                'apellidoPaterno': data['apellidoPaterno'],
                'apelidoMaterno': data['apelidoMaterno'],
                'telefono': data['telefono'],
                'dir_colonia': 'Centro',
                'dir_calle': 'Principal',
                'dir_numero': str(100 + i),
                'tipo_cliente': tipo_fisica if i < 2 else tipo_moral,
                'cuenta': cuenta
            }
        )
        clientes.append(cliente)
        if created:
            print(f"✓ Cliente creado: {cliente.nombre}")

    # Crear tipos de evento
    eventos = []
    for nombre in ['Boda', 'Cumpleaños', 'Corporativo', 'Graduación', 'Baby Shower']:
        tipo, _ = TipoEvento.objects.get_or_create(nombre=nombre, defaults={'disposicion': True})
        eventos.append(tipo)

    # Crear estados de reserva
    estados_reserva = []
    for codigo, nombre in [('PEN', 'Pendiente'), ('CON', 'Confirmada'), ('CAN', 'Cancelada'), ('FIN', 'Finalizada')]:
        estado, _ = EstadoReserva.objects.get_or_create(codigo=codigo, defaults={'nombre': nombre})
        estados_reserva.append(estado)

    # Crear estados de salón
    estado_salon, _ = EstadoSalon.objects.get_or_create(codigo='DIS', defaults={'nombre': 'Disponible'})

    # Crear salones
    salones_data = [
        {'nombre': 'Salón Diamante', 'costo': Decimal('5000.00'), 'ubicacion': 'Piso 1', 'dimenLargo': 20, 'dimenAncho': 15, 'dimenAlto': 4, 'maxCapacidad': 200},
        {'nombre': 'Salón Esmeralda', 'costo': Decimal('3500.00'), 'ubicacion': 'Piso 2', 'dimenLargo': 15, 'dimenAncho': 12, 'dimenAlto': 3, 'maxCapacidad': 150},
        {'nombre': 'Salón Rubí', 'costo': Decimal('2500.00'), 'ubicacion': 'Piso 3', 'dimenLargo': 10, 'dimenAncho': 8, 'dimenAlto': 3, 'maxCapacidad': 80},
    ]

    salones = []
    for data in salones_data:
        salon, created = Salon.objects.get_or_create(
            nombre=data['nombre'],
            defaults={
                'costo': data['costo'],
                'ubicacion': data['ubicacion'],
                'dimenLargo': data['dimenLargo'],
                'dimenAncho': data['dimenAncho'],
                'dimenAlto': data['dimenAlto'],
                'metrosCuadrados': Decimal(str(data['dimenLargo'] * data['dimenAncho'])),
                'maxCapacidad': data['maxCapacidad'],
                'estado_salon': estado_salon
            }
        )
        salones.append(salon)
        if created:
            print(f"✓ Salón creado: {salon.nombre}")

    # Crear tipos de montaje
    tipos_montaje = []
    for nombre in ['Teatro', 'Escuela', 'Banquete', 'Cocktail', 'U']:
        tipo, _ = TipoMontaje.objects.get_or_create(nombre=nombre)
        tipos_montaje.append(tipo)

    # Crear montajes
    montajes = []
    for salon in salones:
        for tipo in tipos_montaje[:2]:
            montaje, created = Montaje.objects.get_or_create(
                salon=salon,
                tipo_montaje=tipo,
                defaults={'costo': Decimal('500.00')}
            )
            montajes.append(montaje)
            if created:
                print(f"✓ Montaje creado: {salon.nombre} - {tipo.nombre}")

    # Crear tipos de servicio
    tipo_servicio_comida, _ = TipoServicio.objects.get_or_create(nombre='Comida', defaults={'disposicion': True})
    tipo_servicio_bebida, _ = TipoServicio.objects.get_or_create(nombre='Bebida', defaults={'disposicion': True})

    # Crear servicios
    servicios_data = [
        {'nombre': 'Buffet Premium', 'descripcion': 'Servicio de buffet con platillos internacionales', 'costo': Decimal('350.00')},
        {'nombre': 'Cóctel de Bienvenida', 'descripcion': 'Selección de cócteles y aperitivos', 'costo': Decimal('200.00')},
        {'nombre': 'Servicio de Barra', 'descripcion': 'Barra libre con bebidas alcohólicas', 'costo': Decimal('450.00')},
        {'nombre': 'Café y Postres', 'descripcion': 'Servicio de café y mesa de postres', 'costo': Decimal('150.00')},
    ]

    servicios = []
    for data in servicios_data:
        servicio, created = Servicio.objects.get_or_create(
            nombre=data['nombre'],
            defaults={
                'descripcion': data['descripcion'],
                'costo': data['costo'],
                'disposicion': True,
                'tipo_servicio': tipo_servicio_comida if 'Comida' in data['nombre'] or 'Buffet' in data['nombre'] else tipo_servicio_bebida
            }
        )
        servicios.append(servicio)
        if created:
            print(f"✓ Servicio creado: {servatorio.nombre}")

    # Crear reservaciones de prueba
    reservaciones_data = [
        {'nombreEvento': 'Boda García-López', 'descripEvento': 'Boda elegante con 150 invitados', 'asistentes': 150},
        {'nombreEvento': 'Cumpleaños 30 de Ana', 'descripEvento': 'Fiesta de cumpleaños con temática tropical', 'asistentes': 50},
        {'nombreEvento': 'Conferencia Tech 2026', 'descripEvento': 'Evento corporativo de tecnología', 'asistentes': 100},
        {'nombreEvento': 'Graduación Martínez', 'descripEvento': 'Celebración de graduación universitaria', 'asistentes': 200},
        {'nombreEvento': 'Baby Shower Rodríguez', 'descripEvento': 'Baby shower para gemelos', 'asistentes': 30},
    ]

    from django.db import transaction
    with transaction.atomic():
        for i, data in enumerate(reservaciones_data):
            cliente = clientes[i % len(clientes)]
            salon = salones[i % len(salones)]
            montaje = Montaje.objects.filter(salon=salon).first()
            tipo_evento = eventos[i % len(eventos)]
            estado = estados_reserva[i % len(estados_reserva)]
            
            fecha_evento = date.today() + timedelta(days=i*7)
            subtotal = Decimal('5000.00') + Decimal(str(i * 500))
            iva = subtotal * Decimal('0.16')
            total = subtotal + iva
            
            reserva, created = Reservacion.objects.get_or_create(
                nombreEvento=data['nombreEvento'],
                defaults={
                    'descripEvento': data['descripEvento'],
                    'estimaAsistentes': data['asistentes'],
                    'fechaEvento': fecha_evento,
                    'horaInicio': time(18, 0),
                    'horaFin': time(23, 0),
                    'subtotal': subtotal,
                    'IVA': iva,
                    'total': total,
                    'cliente': cliente,
                    'montaje': montaje,
                    'estado_reserva': estado,
                    'tipo_evento': tipo_evento,
                }
            )
            
            # Agregar servicios aleatorios
            if created and i % 2 == 0:
                for servicio in servicios[:2]:
                    reserva.reserva_servicio.add(servicio)
            
            if created:
                print(f"✓ Reservación creada: {reserva.nombreEvento}")

    print("\n✓ Datos de prueba creados exitosamente!")

if __name__ == '__main__':
    crear_datos_prueba()
