from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


def paquetes(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    salones = models.Salon.objects.filter(estado_salon='DIS')
    tipos_montaje = models.TipoMontaje.objects.filter(disposicion=True)
    tipos_servicio = models.TipoServicio.objects.filter(disposicion=True)
    tipos_equipamiento = models.TipoEquipa.objects.filter(disposicion=True)
    tipos_mobiliarios = models.TipoMobil.objects.filter(disposicion=True)

    paquetes_list = models.Reservacion.objects.filter(
        es_paquete=True
    ).select_related(
        'montaje__salon', 'montaje__tipo_montaje'
    ).prefetch_related(
        'reservaservicio_set__servicio',
        'reservaequipa_set__equipamiento'
    ).order_by('-id')

    paquetes_con_detalles = []
    for paquete in paquetes_list:
        servicios_count = paquete.reservaservicio_set.count()
        equipamiento_count = paquete.reservaequipa_set.count()
        mobiliario_count = models.MontajeMobiliario.objects.filter(montaje=paquete.montaje).count() if paquete.montaje else 0
        
        paquetes_con_detalles.append({
            'paquete': paquete,
            'servicios_count': servicios_count,
            'equipamiento_count': equipamiento_count,
            'mobiliario_count': mobiliario_count,
        })

    return render(request, "BookingRoomApp/administracion/paquetes.html", {
        "salones": salones,
        "tipos_montaje": tipos_montaje,
        "tipos_servicio": tipos_servicio,
        "tipos_equipamiento": tipos_equipamiento,
        "tipos_mobiliarios": tipos_mobiliarios,
        "rol": rol,
        "paquetes_lista": paquetes_con_detalles,
    })


@csrf_exempt
def crear_paquete(request):
    if request.method == 'POST':
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"DEBUG POST data: {dict(request.POST)}")
            
            data = request.POST
            
            nombre_paquete = data.get('nombre_paquete', '').strip()
            salon_id = data.get('salon_id')
            montaje_id = data.get('montaje_id')
            subtotal = float(data.get('subtotal', 0))
            iva_porcentaje = float(data.get('iva', 16))
            total = float(data.get('total', 0))
            
            servicios_ids = request.POST.getlist('servicios[]')
            logger.error(f"DEBUG servicios_ids: {servicios_ids}")
            
            equipamiento_data = []
            for key, value in request.POST.items():
                logger.error(f"DEBUG key: {key}, value: {value}")
                if key.startswith('equipamiento_') and key.endswith('_id'):
                    index = key.split('_')[1]
                    eq_id = value
                    cantidad = request.POST.get(f'equipamiento_{index}_cantidad', 1)
                    equipamiento_data.append({'id': eq_id, 'cantidad': int(cantidad)})
            
            logger.error(f"DEBUG equipamento_data: {equipamiento_data}")
            
            mobiliario_data = []
            for key, value in request.POST.items():
                if key.startswith('mobiliario_') and key.endswith('_id'):
                    index = key.split('_')[1]
                    mob_id = value
                    cantidad = request.POST.get(f'mobiliario_{index}_cantidad', 1)
                    mobiliario_data.append({'id': mob_id, 'cantidad': int(cantidad)})
            
            logger.error(f"DEBUG mobiliario_data: {mobiliario_data}")
            
            with transaction.atomic():
                estado_plantilla = models.EstadoReserva.objects.get_or_create(
                    codigo='PLANT',
                    defaults={'nombre': 'Plantilla'}
                )[0]
                
                tipo_evento_paquete, _ = models.TipoEvento.objects.get_or_create(
                    nombre='Paquete',
                    defaults={'disposicion': True}
                )
                
                paquete = models.Reservacion.objects.create(
                    nombreEvento=nombre_paquete or 'Paquete sin nombre',
                    nombre_paquete=nombre_paquete,
                    descripEvento=f'Paquete: {nombre_paquete}' if nombre_paquete else 'Paquete sin descripción',
                    estimaAsistentes=0,
                    fechaEvento=None,
                    horaInicio=None,
                    horaFin=None,
                    subtotal=subtotal,
                    IVA=iva_porcentaje,
                    total=total,
                    cliente_id=None,
                    montaje_id=montaje_id if montaje_id else None,
                    estado_reserva=estado_plantilla,
                    tipo_evento=tipo_evento_paquete,
                    es_paquete=True,
                )
                
                for servicio_id in servicios_ids:
                    if servicio_id:
                        models.ReservaServicio.objects.create(
                            reservacion=paquete,
                            servicio_id=servicio_id,
                            extra=False,
                        )
                
                for eq in equipamiento_data:
                    if eq['id']:
                        models.ReservaEquipa.objects.create(
                            reservacion=paquete,
                            equipamiento_id=eq['id'],
                            cantidad=eq['cantidad'],
                            extra=False,
                        )
                
                if montaje_id:
                    for mob in mobiliario_data:
                        if mob['id']:
                            models.MontajeMobiliario.objects.create(
                                montaje_id=montaje_id,
                                mobiliario_id=mob['id'],
                                cantidad=mob['cantidad'],
                            )
            
            return JsonResponse({'success': True, 'message': 'Paquete creado correctamente', 'paquete_id': paquete.id})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@csrf_exempt
def editar_paquete(request, pk):
    if request.method == 'POST':
        try:
            paquete = get_object_or_404(models.Reservacion, pk=pk, es_paquete=True)
            data = request.POST
            
            nombre_paquete = data.get('nombre_paquete', '').strip()
            salon_id = data.get('salon_id')
            montaje_id = data.get('montaje_id')
            subtotal = float(data.get('subtotal', 0))
            iva_porcentaje = float(data.get('iva', 16))
            total = float(data.get('total', 0))
            
            servicios_ids = request.POST.getlist('servicios[]')
            equipamiento_data = []
            for key, value in request.POST.items():
                if key.startswith('equipamiento_') and key.endswith('_id'):
                    index = key.split('_')[1]
                    eq_id = value
                    cantidad = request.POST.get(f'equipamiento_{index}_cantidad', 1)
                    equipamiento_data.append({'id': eq_id, 'cantidad': int(cantidad)})
            
            mobiliario_data = []
            for key, value in request.POST.items():
                if key.startswith('mobiliario_') and key.endswith('_id'):
                    index = key.split('_')[1]
                    mob_id = value
                    cantidad = request.POST.get(f'mobiliario_{index}_cantidad', 1)
                    mobiliario_data.append({'id': mob_id, 'cantidad': int(cantidad)})
            
            with transaction.atomic():
                paquete.nombreEvento = nombre_paquete or 'Paquete sin nombre'
                paquete.nombre_paquete = nombre_paquete
                paquete.descripEvento = f'Paquete: {nombre_paquete}' if nombre_paquete else 'Paquete sin descripción'
                paquete.subtotal = subtotal
                paquete.IVA = iva_porcentaje
                paquete.total = total
                paquete.montaje_id = montaje_id if montaje_id else None
                paquete.save()
                
                paquete.reservaservicio_set.all().delete()
                for servicio_id in servicios_ids:
                    if servicio_id:
                        models.ReservaServicio.objects.create(
                            reservacion=paquete,
                            servicio_id=servicio_id,
                            extra=False,
                        )
                
                paquete.reservaequipa_set.all().delete()
                for eq in equipamiento_data:
                    if eq['id']:
                        models.ReservaEquipa.objects.create(
                            reservacion=paquete,
                            equipamiento_id=eq['id'],
                            cantidad=eq['cantidad'],
                            extra=False,
                        )
                
                if paquete.montaje:
                    models.MontajeMobiliario.objects.filter(montaje=paquete.montaje).delete()
                
                if montaje_id:
                    for mob in mobiliario_data:
                        if mob['id']:
                            models.MontajeMobiliario.objects.create(
                                montaje_id=montaje_id,
                                mobiliario_id=mob['id'],
                                cantidad=mob['cantidad'],
                            )
            
            return JsonResponse({'success': True, 'message': 'Paquete actualizado correctamente'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@csrf_exempt
def eliminar_paquete(request, pk):
    if request.method == 'POST':
        try:
            paquete = get_object_or_404(models.Reservacion, pk=pk, es_paquete=True)
            
            with transaction.atomic():
                if paquete.montaje:
                    models.MontajeMobiliario.objects.filter(montaje=paquete.montaje).delete()
                paquete.reservaservicio_set.all().delete()
                paquete.reservaequipa_set.all().delete()
                paquete.delete()
            
            return JsonResponse({'success': True, 'message': 'Paquete eliminado correctamente'})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


@csrf_exempt
def duplicar_paquete(request, pk):
    if request.method == 'POST':
        try:
            paquete_original = get_object_or_404(models.Reservacion, pk=pk, es_paquete=True)
            
            with transaction.atomic():
                nuevo_paquete = models.Reservacion.objects.create(
                    nombreEvento=f"{paquete_original.nombre_paquete} (Copia)",
                    nombre_paquete=f"{paquete_original.nombre_paquete} (Copia)",
                    descripEvento=paquete_original.descripEvento,
                    estimaAsistentes=0,
                    fechaEvento=None,
                    horaInicio=None,
                    horaFin=None,
                    subtotal=paquete_original.subtotal,
                    IVA=paquete_original.IVA,
                    total=paquete_original.total,
                    cliente_id=None,
                    montaje_id=paquete_original.montaje_id,
                    estado_reserva=paquete_original.estado_reserva,
                    tipo_evento=paquete_original.tipo_evento,
                    es_paquete=True,
                )
                
                for servicio in paquete_original.reservaservicio_set.all():
                    models.ReservaServicio.objects.create(
                        reservacion=nuevo_paquete,
                        servicio=servicio.servicio,
                        extra=servicio.extra,
                    )
                
                for equipamiento in paquete_original.reservaequipa_set.all():
                    models.ReservaEquipa.objects.create(
                        reservacion=nuevo_paquete,
                        equipamiento=equipamiento.equipamiento,
                        cantidad=equipamiento.cantidad,
                        extra=equipamiento.extra,
                    )
                
                if paquete_original.montaje:
                    for mob in models.MontajeMobiliario.objects.filter(montaje=paquete_original.montaje):
                        models.MontajeMobiliario.objects.create(
                            montaje=paquete_original.montaje,
                            mobiliario=mob.mobiliario,
                            cantidad=mob.cantidad,
                        )
            
            return JsonResponse({'success': True, 'message': 'Paquete duplicado correctamente', 'paquete_id': nuevo_paquete.id})
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)


def obtener_detalle_paquete(request, pk):
    if request.method == 'GET':
        try:
            paquete = get_object_or_404(models.Reservacion, pk=pk, es_paquete=True)
            
            servicios = list(paquete.reservaservicio_set.select_related('servicio__tipo_servicio').values(
                'servicio__id', 'servicio__nombre', 'servicio__costo', 'servicio__tipo_servicio__nombre'
            ))
            
            equipamiento = list(paquete.reservaequipa_set.select_related('equipamiento__tipo_equipa').values(
                'equipamiento__id', 'equipamiento__nombre', 'equipamiento__costo', 'cantidad', 'equipamiento__tipo_equipa__nombre'
            ))
            
            mobiliario = []
            if paquete.montaje:
                mobiliario = list(models.MontajeMobiliario.objects.filter(montaje=paquete.montaje).select_related('mobiliario__tipo_movil').values(
                    'mobiliario__id', 'mobiliario__nombre', 'mobiliario__costo', 'cantidad', 'mobiliario__tipo_movil__nombre'
                ))
            
            return JsonResponse({
                'success': True,
                'paquete': {
                    'id': paquete.id,
                    'nombre_paquete': paquete.nombre_paquete,
                    'salon_id': paquete.montaje.salon.id if paquete.montaje else None,
                    'salon_nombre': paquete.montaje.salon.nombre if paquete.montaje else None,
                    'montaje_id': paquete.montaje.id if paquete.montaje else None,
                    'montaje_nombre': paquete.montaje.tipo_montaje.nombre if paquete.montaje else None,
                    'subtotal': str(paquete.subtotal),
                    'iva': str(paquete.IVA),
                    'total': str(paquete.total),
                },
                'servicios': servicios,
                'equipamiento': equipamiento,
                'mobiliario': mobiliario,
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
