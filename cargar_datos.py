import os
import sys
import django
from datetime import date, time, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookingRoom_Django.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from BookingRoomApp import models

def main():
    print("="*60)
    print("🚀 INICIANDO CARGA DE DATOS (ORM)")
    print("="*60)

    # 1. Catálogos
    print("📦 Creando catálogos...")
    try:
        r_recep, _ = models.Rol.objects.get_or_create(codigo='RECEP', defaults={'nombre': 'Recepcionista'})
        tc_mor, _ = models.TipoCliente.objects.get_or_create(codigo='MOR', defaults={'nombre': 'Persona moral'})
        tc_fis, _ = models.TipoCliente.objects.get_or_create(codigo='FIS', defaults={'nombre': 'Persona fisica'})
        e_act, _ = models.EstadoCuenta.objects.get_or_create(codigo='ACT', defaults={'nombre': 'Activa'})
        
        es_dis, _ = models.EstadoSalon.objects.get_or_create(codigo='DIS', defaults={'nombre': 'Disponible'})
        
        er_pen, _ = models.EstadoReserva.objects.get_or_create(codigo='PEN', defaults={'nombre': 'Pendiente'})
        er_conf, _ = models.EstadoReserva.objects.get_or_create(codigo='CONF', defaults={'nombre': 'Confirmada'})
        
        tmont1, _ = models.TipoMontaje.objects.get_or_create(nombre='Teatro', defaults={'capacidadIdeal': 100})
        tmont3, _ = models.TipoMontaje.objects.get_or_create(nombre='Banquete', defaults={'capacidadIdeal': 80})
        tmont6, _ = models.TipoMontaje.objects.get_or_create(nombre='Herradura', defaults={'capacidadIdeal': 50})

        te1, _ = models.TipoEvento.objects.get_or_create(nombre='Conferencia')
        te5, _ = models.TipoEvento.objects.get_or_create(nombre='Boda')
        te6, _ = models.TipoEvento.objects.get_or_create(nombre='Junta de consejo')
        te12, _ = models.TipoEvento.objects.get_or_create(nombre='XV Anos')
        te16, _ = models.TipoEvento.objects.get_or_create(nombre='Aniversario')
        te17, _ = models.TipoEvento.objects.get_or_create(nombre='Gala')

        cp_abon, _ = models.ConceptoPago.objects.get_or_create(codigo='ABONO', defaults={'nombre': 'Abono'})
        cp_liq, _ = models.ConceptoPago.objects.get_or_create(codigo='LIQUI', defaults={'nombre': 'Liquidacion'})
        
        mp_tarj, _ = models.MetodoPago.objects.get_or_create(codigo='TARJE', defaults={'nombre': 'Tarjeta'})
        mp_trans, _ = models.MetodoPago.objects.get_or_create(codigo='TRANS', defaults={'nombre': 'Transferencia'})

        ts1, _ = models.TipoServicio.objects.get_or_create(nombre='Catering')
        ts7, _ = models.TipoServicio.objects.get_or_create(nombre='Seguridad')

        te_audio, _ = models.TipoEquipa.objects.get_or_create(nombre='Audio')
        te_luz, _ = models.TipoEquipa.objects.get_or_create(nombre='Iluminacion')

        tm_silla, _ = models.TipoMobil.objects.get_or_create(nombre='Sillas')
        tm_mesa, _ = models.TipoMobil.objects.get_or_create(nombre='Mesas Redondas')

    except Exception as e:
        print(f"❌ Error creando catálogos: {e}")
        return

    # 2. Usuarios y Cuentas
    print("👥 Creando usuarios y clientes...")

    try:
        # Cuentas de trabajadores
        c_admin, _ = models.Cuenta.objects.get_or_create(correo_electronico='admin@hotel.com', defaults={'nombre_usuario': 'admin_test', 'estado_cuenta': e_act})
        c_recep, _ = models.Cuenta.objects.get_or_create(correo_electronico='recep@hotel.com', defaults={'nombre_usuario': 'carlos_recep', 'estado_cuenta': e_act})

        trabajador, _ = models.Trabajador.objects.get_or_create(
            no_empleado='TRAB-001', 
            defaults={
                'rfc': 'XAXX010101000', 'nombre': 'Carlos', 
                'apellidoPaterno': 'Recepcionista', 'telefono': '5550000000', 
                'correo_electronico': 'recep@hotel.com', 'rol': r_recep, 'cuenta': c_recep
            }
        )

        # Cuentas de clientes
        def crear_cliente(email, nombre, tipo):
            cuenta, _ = models.Cuenta.objects.get_or_create(correo_electronico=email, defaults={'nombre_usuario': email.split('@')[0], 'estado_cuenta': e_act})
            cliente, _ = models.DatosCliente.objects.get_or_create(
                correo_electronico=email,
                defaults={
                    'cuenta': cuenta,
                    'nombre': nombre,
                    'apellidoPaterno': 'Apellido',
                    'telefono': '5551234567',
                    'rfc': 'XAXX010101000',
                    'nombre_fiscal': nombre,
                    'dir_colonia': 'Centro',
                    'dir_calle': 'Calle 1',
                    'dir_numero': '100',
                    'tipo_cliente': tipo
                }
            )
            return cliente

        cl_corp = crear_cliente('corp@industrial.mx', 'Corporativo Industrial', tc_mor)
        cl_ana = crear_cliente('ana@wedding.com', 'Ana Martinez', tc_fis)
        cl_rob = crear_cliente('rob@xv.com', 'Roberto Sanchez', tc_fis)
        cl_event = crear_cliente('info@events.com', 'Events Planner', tc_mor)
        cl_fiest = crear_cliente('contacto@fiestas.com', 'Fiestas Deluxe', tc_mor)

    except Exception as e:
        print(f"❌ Error creando usuarios: {e}")
        return

    # 3. Servicios y Equipamiento
    print("🎒 Creando servicios y equipamiento...")
    
    try:
        s_coffee, _ = models.Servicio.objects.get_or_create(nombre='Coffee Break', defaults={'tipo_servicio': ts1, 'costo': 1500, 'disposicion': True})
        s_dj, _ = models.Servicio.objects.get_or_create(nombre='DJ y Musica', defaults={'tipo_servicio': ts7, 'costo': 4500, 'disposicion': True})
        
        eq_proy, _ = models.Equipamiento.objects.get_or_create(nombre='Proyector HD', defaults={'tipo_equipa': te_luz, 'costo': 500, 'stock': 10})
        eq_mic, _ = models.Equipamiento.objects.get_or_create(nombre='Microfono', defaults={'tipo_equipa': te_audio, 'costo': 200, 'stock': 20})

        mob_silla, _ = models.Mobiliario.objects.get_or_create(nombre='Silla Tiffany', defaults={'tipo_movil': tm_silla, 'costo': 50, 'stock': 200})
        mob_mesa, _ = models.Mobiliario.objects.get_or_create(nombre='Mesa Redonda', defaults={'tipo_movil': tm_mesa, 'costo': 100, 'stock': 50})
    except Exception as e:
        print(f"❌ Error creando activos: {e}")
        return

    # 4. Salones y Montajes
    print("🏛️ Creando salones...")
    
    try:
        salon1, _ = models.Salon.objects.get_or_create(
            nombre='Salon Gran Gala', 
            defaults={'costo': 15000, 'estado_salon': es_dis, 'maxCapacidad': 200, 
                      'dimenLargo': 25, 'dimenAncho': 15, 'dimenAlto': 4, 'metrosCuadrados': 375}
        )
        salon2, _ = models.Salon.objects.get_or_create(
            nombre='Salon Ejecutivo',
            defaults={'costo': 6000, 'estado_salon': es_dis, 'maxCapacidad': 60,
                      'dimenLargo': 12, 'dimenAncho': 8, 'dimenAlto': 2.8, 'metrosCuadrados': 96}
        )

        montaje1, _ = models.Montaje.objects.get_or_create(salon=salon1, tipo_montaje=tmont3, defaults={'costo': 3000})
        montaje2, _ = models.Montaje.objects.get_or_create(salon=salon2, tipo_montaje=tmont6, defaults={'costo': 1500})
    except Exception as e:
        print(f"❌ Error creando salones: {e}")
        return

    # 5. Reservaciones
    print("📅 Creando reservaciones...")
    hoy = date.today()
    futuro = hoy + timedelta(days=20)

    try:
        def crear_reserva(cliente, montaje, estado, evento, fecha, total, nombre):
            r = models.Reservacion.objects.create(
                nombreEvento=nombre,
                cliente=cliente, montaje=montaje, estado_reserva=estado,
                tipo_evento=evento, trabajador=trabajador,
                fechaReservacion=hoy, fechaEvento=fecha,
                horaInicio=time(10,0), horaFin=time(14,0),
                subtotal=total/1.16, IVA=total*0.16/1.16, total=total,
                estimaAsistentes=50
            )
            return r

        # 3 del Cliente 1
        r1 = crear_reserva(cl_corp, montaje1, er_conf, te1, futuro, 52200, 'Conferencia Anual')
        r2 = crear_reserva(cl_corp, montaje2, er_pen, te6, futuro, 20880, 'Junta Directiva')
        r3 = crear_reserva(cl_corp, montaje1, er_pen, te12, futuro, 37120, 'Seminario Tech')

        # 4 de otros
        r4 = crear_reserva(cl_ana, montaje1, er_conf, te5, futuro, 98600, 'Boda Ana')
        r5 = crear_reserva(cl_rob, montaje2, er_pen, te17, futuro, 71920, 'XV Años')
        r6 = crear_reserva(cl_event, montaje1, er_conf, te16, futuro, 145000, 'Gala 2026')
        r7 = crear_reserva(cl_fiest, montaje2, er_pen, te5, futuro, 63800, 'Aniversario')

    except Exception as e:
        print(f"❌ Error creando reservaciones: {e}")
        return

    # 6. Pagos
    print("💰 Registrando pagos...")
    
    def hacer_pago(reserva, monto, concepto, metodo, no_pago):
        try:
            models.Pago.objects.create(
                reservacion=reserva, nota=f'Pago {no_pago}', monto=monto, 
                no_pago=no_pago, concepto_pago=concepto, metodo_pago=metodo, saldo=0
            )
        except Exception as e:
            print(f"   ⚠️ Error en pago {no_pago} de {reserva.nombreEvento}: {e}")

    # Pagos de R1 (Completa)
    hacer_pago(r1, 26100, cp_abon, mp_tarj, 1)
    hacer_pago(r1, 26100, cp_liq, mp_tarj, 2)

    # Abonos a las demás
    pagos_list = [
        (r2, 10440, mp_trans, 1),
        (r3, 18560, mp_tarj, 1),
        (r4, 49300, mp_tarj, 1),
        (r5, 35960, mp_tarj, 1),
        (r6, 72500, mp_trans, 1),
        (r7, 31900, mp_tarj, 1),
    ]
    
    for r, monto, metodo, no in pagos_list:
        hacer_pago(r, monto, cp_abon, metodo, no)

    print("="*60)
    print("✅ ¡DATOS CARGADOS EXITOSAMENTE!")
    print("="*60)

if __name__ == '__main__':
    main()
