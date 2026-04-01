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
        )
        estados = models.EstadoReserva.objects.all()
        reservacion_total = models.Reservacion.objects.count()

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

        return render(request, self.template_name, {
            "tipos_servicio": models.TipoServicio.objects.filter(disposicion=True),
            "tipos_equipa": models.TipoEquipa.objects.filter(disposicion=True),
            "tipos_equipamiento": models.TipoEquipa.objects.filter(disposicion=True),
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
        equipamientos = models.Equipamiento.objects.filter(
            tipo_equipa_id=tipo_id, stock__gt=0
        ).values('id', 'nombre', 'costo', 'stock')
        return JsonResponse({'equipamientos': list(equipamientos)})


class DetallesReservacionView(generic.DetailView):
    template_name = "BookingRoomApp/home/"
    model = models.Reservacion
    context_object_name = "reservacion"


def reservacion_detalle_json(request, pk):
    reserva = get_object_or_404(
        models.Reservacion.objects.select_related(
            "cliente", "montaje__salon", "montaje__tipo_montaje", "estado_reserva", "tipo_evento",
        ),
        pk=pk,
    )
    return JsonResponse({
        "id": reserva.pk, "nombre_evento": reserva.nombreEvento,
        "descripcion": reserva.descripEvento, "fecha": reserva.fechaEvento.isoformat(),
        "hora_inicio": reserva.horaInicio.strftime("%H:%M"),
        "hora_fin": reserva.horaFin.strftime("%H:%M"),
        "estado": reserva.estado_reserva.nombre, "asistentes": reserva.estimaAsistentes,
        "salon": reserva.montaje.salon.nombre if reserva.montaje and reserva.montaje.salon else "N/A",
        "montaje": reserva.montaje.tipo_montaje.nombre if reserva.montaje and reserva.montaje.tipo_montaje else "N/A",
        "tipo_evento": reserva.tipo_evento.nombre if reserva.tipo_evento else "N/A",
        "subtotal": str(reserva.subtotal), "iva": str(reserva.IVA), "total": str(reserva.total),
        "cliente": {
            "nombre": reserva.cliente.nombre, "apellido_paterno": reserva.cliente.apellidoPaterno,
            "apellido_materno": reserva.cliente.apelidoMaterno or "",
            "correo": reserva.cliente.correo_electronico, "telefono": reserva.cliente.telefono,
            "rfc": reserva.cliente.rfc, "nombre_fiscal": reserva.cliente.nombre_fiscal,
        },
        "servicios": list(reserva.reservaservicio_set.values_list("servicio__nombre", flat=True)),
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