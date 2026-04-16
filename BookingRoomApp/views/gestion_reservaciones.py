from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


class HistorialReservacionViw(generic.View):
    template_name = "BookingRoomApp/recepcion/historial_reservacion.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        reservaciones = models.Reservacion.objects.select_related(
            "cliente", "estado_reserva", "montaje__salon",
        ).filter(es_paquete=False).exclude(estado_reserva__codigo='SOLIC')
        estados = models.EstadoReserva.objects.all()
        reservacion_total = models.Reservacion.objects.filter(es_paquete=False).count()

        nombre = request.GET.get('nombre', '')
        estado_filtro = request.GET.get('estado', '')
        
        if nombre:
            reservaciones = reservaciones.filter(
                Q(nombreEvento__icontains=nombre) |
                Q(cliente__nombre__icontains=nombre)
            )
        
        if estado_filtro:
            reservaciones = reservaciones.filter(estado_reserva__codigo=estado_filtro)

        return render(request, self.template_name, {
            "reservaciones": reservaciones.order_by('-id').all(),
            "estados": estados,
            "rol": rol,
            "nombre": nombre,
            "estado_filtro": estado_filtro,
            "reservacion_total": reservacion_total
        })


class ReservacionView(generic.View):
    template_name = "BookingRoomApp/recepcion/reservacion.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        trabajador = models.Trabajador.objects.get(cuenta=cuenta.pk)

        reservaciones_solicitudes = models.Reservacion.objects.filter(
            estado_reserva__codigo='SOLIC'
        ).select_related(
            "cliente", "estado_reserva", "montaje__salon"
        ).order_by('-id')

        return render(request, self.template_name, {
            "tipos_evento": models.TipoEvento.objects.all(),
            "trabajador_id": trabajador.pk,
            "trabajador_no_empleado": trabajador.no_empleado,
            "tipos_mobiliarios": models.TipoMobil.objects.filter(disposicion=True),
            "salones": models.Salon.objects.all(),
            "tipos_servicio": models.TipoServicio.objects.filter(disposicion=True),
            "tipos_equipa": models.TipoEquipa.objects.filter(disposicion=True),
            "tipos_equipamiento": models.TipoEquipa.objects.filter(disposicion=True),
            "tipos_montaje": models.TipoMontaje.objects.filter(disposicion=True),
            "rol": rol,
            "reservaciones_solicitudes": reservaciones_solicitudes,
        })


class ReservacionClienteView(generic.View):
    template_name = "BookingRoomApp/cliente/reservacion_cliente.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        return render(request, self.template_name, {
            "tipos_evento": models.TipoEvento.objects.all(),
            "trabajador_id": "",  # Cliente no tiene trabajador
            "trabajador_no_empleado": "",
            "cliente_email": cuenta.correo_electronico,  # Email para cargar datos
            "tipos_mobiliarios": models.TipoMobil.objects.filter(disposicion=True),
            "salones": models.Salon.objects.filter(estado_salon='DIS'),
            "tipos_servicio": models.TipoServicio.objects.filter(disposicion=True),
            "tipos_equipa": models.TipoEquipa.objects.filter(disposicion=True),
            "tipos_equipamiento": models.TipoEquipa.objects.filter(disposicion=True),
            "tipos_montaje": models.TipoMontaje.objects.filter(disposicion=True),
            "rol": rol,
        })


@csrf_exempt
def buscar_cliente(request):
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse({'encontrado': False, 'mensaje': 'Ingrese un RFC o nombre'})
        
        cliente = models.DatosCliente.objects.filter(rfc__iexact=query).first()
        if not cliente:
            cliente = models.DatosCliente.objects.filter(
                Q(nombre__icontains=query) | Q(nombre_fiscal__icontains=query)
            ).first()
        
        if cliente:
            return JsonResponse({
                'encontrado': True,
                'cliente': {
                    'id': cliente.id, 'rfc': cliente.rfc, 'nombre': cliente.nombre,
                    'apellido_paterno': cliente.apellidoPaterno,
                    'apellido_materno': cliente.apelidoMaterno or '',
                    'nombre_fiscal': cliente.nombre_fiscal,
                    'telefono': cliente.telefono, 'correo': cliente.correo_electronico,
                    'colonia': cliente.dir_colonia, 'calle': cliente.dir_calle,
                    'numero': cliente.dir_numero,
                    'tipo_cliente': cliente.tipo_cliente.nombre if cliente.tipo_cliente else '',
                }
            })
        
        return JsonResponse({'encontrado': False, 'mensaje': 'Cliente no encontrado'})


@csrf_exempt
def obtener_servicios_por_tipo(request):
    if request.method == 'GET':
        tipo_id = request.GET.get('tipo_id')
        if not tipo_id:
            return JsonResponse({'servicios': []})
        servicios = models.Servicio.objects.filter(
            tipo_servicio_id=tipo_id, disposicion=True
        ).values('id', 'nombre', 'costo')
        return JsonResponse({'servicios': list(servicios)})


@csrf_exempt
def obtener_equipamiento_por_tipo(request):
    if request.method == 'GET':
        tipo_id = request.GET.get('tipo_id')
        if not tipo_id:
            return JsonResponse({'equipamientos': []})
        
        inventarios = models.InventarioEquipa.objects.filter(
            estado_equipa='DISP',
            equipamiento__tipo_equipa_id=tipo_id
        ).select_related('equipamiento')

        lista_equipos = []
        for item in inventarios:
            if item.cantidad > 0:
                lista_equipos.append({
                    'id': item.equipamiento.id,
                    'nombre': item.equipamiento.nombre,
                    'costo': item.equipamiento.costo,
                    'stock': item.cantidad
                })

        return JsonResponse({'equipamientos': lista_equipos})


@csrf_exempt
def mobiliarios_por_tipo(request):
    if request.method == 'GET':
        tipo_id = request.GET.get('tipo_id')

        if not tipo_id:
            return JsonResponse({'mobiliarios': []})
        try:

            inventarios = models.InventarioMob.objects.filter(
                estado_mobil='DISP',
                mobiliario__tipo_movil_id=tipo_id
            ).select_related('mobiliario')

            lista_mobiliarios = []
            for item in inventarios:
                if item.cantidad > 0:
                    lista_mobiliarios.append({
                        'id': item.mobiliario.id,
                        'nombre': item.mobiliario.nombre,
                        'costo': str(item.mobiliario.costo),
                        'stock': item.cantidad
                    })

            return JsonResponse({'mobiliarios': lista_mobiliarios})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def montaje_por_capacidad_salon(request):
    salonId = request.GET.get('salon_id')
    if not salonId:
        return JsonResponse({'montajes': []})
    
    try:
        salon = models.Salon.objects.get(id=salonId)
        tipos_montajes = models.TipoMontaje.objects.filter(capacidadIdeal__lte=salon.maxCapacidad)
        lista = []
        for tipo in tipos_montajes:
            lista.append({
                'id': tipo.id,
                'nombre': tipo.nombre,
                'capacidadIdeal': tipo.capacidadIdeal
            })

        return JsonResponse({'montajes': lista, 'salon': {'costo': str(salon.costo)}})
    except models.Salon.DoesNotExist:
        return JsonResponse({'error': 'Salón no encontrado'}, status=404)


@csrf_exempt
def montaje_por_salon(request):
    salonId = request.GET.get('salon_id')
    todos = request.GET.get('todos')
    
    if todos == 'true':
        montajes = models.Montaje.objects.select_related('tipo_montaje', 'salon')
        lista = []
        for m in montajes:
            lista.append({
                'id': m.id,
                'tipo_montaje_id': m.tipo_montaje.id,
                'nombre': f'{m.tipo_montaje.nombre} - {m.salon.nombre}',
                'capacidadIdeal': m.tipo_montaje.capacidadIdeal,
                'costo': str(m.costo),
                'salon_nombre': m.salon.nombre
            })

        if len(lista) == 0:
            tipos_montaje = models.TipoMontaje.objects.prefetch_related()

        return JsonResponse({'montajes': lista})
    
    if not salonId:
        return JsonResponse({'montajes': []})
    
    try:
        salon = models.Salon.objects.get(id=salonId)
        
        # Obtener los Montaje relacionados con este salon
        montajes = models.Montaje.objects.filter(salon=salon).select_related('tipo_montaje')

        lista = []
        for m in montajes:
            lista.append({
                'id': m.id,
                'tipo_montaje_id': m.tipo_montaje.id,
                'nombre': m.tipo_montaje.nombre,
                'capacidadIdeal': m.tipo_montaje.capacidadIdeal,
                'costo': str(m.costo)
            })
        
        return JsonResponse({
            'montajes': lista,
            'salon': {
                'id': salon.id,
                'nombre': salon.nombre,
                'costo': str(salon.costo),
                'capacidad': salon.maxCapacidad
            }
        })

    except models.Salon.DoesNotExist:
        return JsonResponse({'error': 'Salón no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


class DetallesReservacionView(generic.DetailView):
    template_name = "BookingRoomApp/home/"
    model = models.Reservacion
    context_object_name = "reservacion"


def reservacion_detalle_json(request, pk):
    reserva = get_object_or_404(
        models.Reservacion.objects.select_related(
            "cliente", "montaje__salon", "montaje__tipo_montaje", "estado_reserva", "tipo_evento", "trabajador",
        ),
        pk=pk,
    )

    # Servicios: lista de nombres
    servicios = list(reserva.reservaservicio_set.values_list("servicio__nombre", flat=True))
    
    # Equipamientos: lista con nombre y cantidad
    equipamientos = list(reserva.reservaequipa_set.select_related('equipamiento').values(
        'equipamiento__nombre', 'cantidad'
    ))
    # Formatear equipamientos para el frontend
    equipamientos_formatted = [
        {'nombre': eq['equipamiento__nombre'], 'cantidad': eq['cantidad']}
        for eq in equipamientos
    ]

    # Mobiliarios: lista con nombre y cantidad
    mobiliario = []
    if reserva.montaje:
        mobiliario_qs = models.MontajeMobiliario.objects.filter(
            montaje=reserva.montaje
        ).select_related('mobiliario').values('mobiliario__nombre', 'cantidad')
        mobiliario = [
            {'nombre': mob['mobiliario__nombre'], 'cantidad': mob['cantidad']}
            for mob in mobiliario_qs
        ]

    return JsonResponse({
        "id": reserva.pk, "nombre_evento": reserva.nombreEvento,
        "descripcion": reserva.descripEvento, "fecha": reserva.fechaEvento.isoformat() if reserva.fechaEvento else None,
        "hora_inicio": reserva.horaInicio.strftime("%H:%M") if reserva.horaInicio else None,
        "hora_fin": reserva.horaFin.strftime("%H:%M") if reserva.horaFin else None,
        "estado": reserva.estado_reserva.nombre, "estado_codigo": reserva.estado_reserva.codigo,
        "asistentes": reserva.estimaAsistentes,
        "salon": reserva.montaje.salon.nombre if reserva.montaje and reserva.montaje.salon else "N/A",
        "montaje": reserva.montaje.tipo_montaje.nombre if reserva.montaje and reserva.montaje.tipo_montaje else "N/A",
        "tipo_evento": reserva.tipo_evento.nombre if reserva.tipo_evento else "N/A",
        "subtotal": str(reserva.subtotal), "iva": str(reserva.IVA), "total": str(reserva.total),
        "trabajador": reserva.trabajador.nombre if reserva.trabajador else None,
        "cliente": {
            "nombre": reserva.cliente.nombre, "apellido_paterno": reserva.cliente.apellidoPaterno,
            "apellido_materno": reserva.cliente.apelidoMaterno or "",
            "correo": reserva.cliente.correo_electronico, "telefono": reserva.cliente.telefono,
            "rfc": reserva.cliente.rfc, "nombre_fiscal": reserva.cliente.nombre_fiscal,
        },
        "servicios": servicios,
        "equipamientos": equipamientos_formatted,
        "mobiliarios": mobiliario,
    })


def historial_detalle(request, pk):
    reservacion = get_object_or_404(models.Reservacion, pk=pk)
    pagos = models.Pago.objects.filter(reservacion=reservacion).order_by("no_pago")
    
    primer_pago = segundo_pago = 0
    for pago in pagos:
        if pago.no_pago == 1:
            primer_pago = pago.monto
        elif pago.no_pago == 2:
            segundo_pago = pago.monto
    
    ultimo_pago = pagos.order_by("-no_pago").first()
    saldo = ultimo_pago.saldo if ultimo_pago else reservacion.total
    
    return JsonResponse({
        "total": str(reservacion.total), "subtotal": str(reservacion.subtotal),
        "iva": str(reservacion.IVA), "primer_pago": str(primer_pago),
        "segundo_pago": str(segundo_pago), "saldo": str(saldo),
    })


@csrf_exempt
def confirmar_reservacion(request, pk):
    if request.method == 'POST':
        try:
            reserva = get_object_or_404(models.Reservacion, pk=pk)

            # Obtener el trabajador actual desde la sesión
            cuenta, rol = get_cuenta_and_rol(request)
            if not cuenta:
                return JsonResponse({'success': False, 'message': 'No hay sesión activa'}, status=400)
            
            # Buscar el trabajador asociado a esta cuenta
            try:
                trabajador = models.Trabajador.objects.get(cuenta=cuenta)
            except models.Trabajador.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'No hay trabajador asociado a esta cuenta'}, status=400)

            # Actualizar descripción si se proporciona
            descripcion = request.POST.get('descripcion', '')
            if descripcion:
                reserva.descripEvento = descripcion

            # Confirmar la reservación
            reserva.estado_reserva = models.EstadoReserva.objects.get(codigo='CON')
            reserva.trabajador = trabajador
            reserva.save()

            return JsonResponse({'success': True, 'message': 'Reservación confirmada'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@csrf_exempt
def cancelar_reservacion(request, pk):
    if request.method == 'POST':
        try:
            reserva = get_object_or_404(models.Reservacion, pk=pk)
            
            # Cancelar la reservación
            reserva.estado_reserva = models.EstadoReserva.objects.get(codigo='CAN')
            reserva.save()
            
            return JsonResponse({'success': True, 'message': 'Reservación cancelada'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)




@csrf_exempt
def actualizar_reservacion(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                reservacion = models.Reservacion.objects.select_related('cliente').get(pk=pk)
                cliente = reservacion.cliente

                if request.POST.get('cliente_nombre'):
                    cliente.nombre = request.POST.get('cliente_nombre')
                if request.POST.get('cliente_apellido_paterno'):
                    cliente.apellidoPaterno = request.POST.get('cliente_apellido_paterno')
                if request.POST.get('cliente_apellido_materno'):
                    cliente.apelidoMaterno = request.POST.get('cliente_apellido_materno')
                if request.POST.get('cliente_correo'):
                    cliente.correo_electronico = request.POST.get('cliente_correo')
                if request.POST.get('cliente_telefono'):
                    cliente.telefono = request.POST.get('cliente_telefono')
                if request.POST.get('cliente_rfc'):
                    cliente.rfc = request.POST.get('cliente_rfc')
                if request.POST.get('cliente_nombre_fiscal'):
                    cliente.nombre_fiscal = request.POST.get('cliente_nombre_fiscal')
                cliente.save()

                if request.POST.get('evento_nombre'):
                    reservacion.nombreEvento = request.POST.get('evento_nombre')
                if request.POST.get('evento_descripcion'):
                    reservacion.descripEvento = request.POST.get('evento_descripcion')
                if request.POST.get('evento_fecha'):
                    reservacion.fechaEvento = request.POST.get('evento_fecha')
                if request.POST.get('evento_hora_inicio'):
                    reservacion.horaInicio = request.POST.get('evento_hora_inicio')
                if request.POST.get('evento_hora_fin'):
                    reservacion.horaFin = request.POST.get('evento_hora_fin')
                if request.POST.get('evento_asistentes'):
                    reservacion.estimaAsistentes = request.POST.get('evento_asistentes')

                estado_codigo = request.POST.get('evento_estado', '')
                if estado_codigo:
                    reservacion.estado_reserva = models.EstadoReserva.objects.get(codigo=estado_codigo)

                reservacion.save()

            messages.success(request, 'Reservación actualizada correctamente')
            return JsonResponse({'success': True, 'redirect': reverse('historial_reservacion')})
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)