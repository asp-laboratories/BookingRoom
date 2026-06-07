from django.http import JsonResponse
from django.db.models import Q
from BookingRoomApp import models
from datetime import datetime


def verificar_salon_disponible(request):
    """
    Verifica la disponibilidad de salones para una fecha específica.
    Usa la misma lógica que la API de Flutter: SalonService.getSalonesDisponibles()
    - Solo DIS y DISP son disponibles
    - Cualquier otro código (LIMPI, NODIS, MANTE, RESV, OCUP) bloquea el salón
    """
    fecha_str = request.GET.get('fecha')
    
    if not fecha_str:
        return JsonResponse({
            'success': False,
            'message': 'Fecha es requerida'
        })
    
    try:
        fecha_evento = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Formato de fecha inválido'
        })
    
    salones = models.Salon.objects.select_related('estado_salon').all()
    
    salon_ids_ocupados = set(
        models.Reservacion.objects.filter(
            fechaEvento=fecha_evento,
            estado_reserva__codigo__in=['CONF', 'CON']
        ).values_list('montaje__salon_id', flat=True).distinct()
    )
    
    estados_fecha = {}
    registros = models.RegistrEstadSalon.objects.filter(
        fecha=fecha_evento
    ).select_related('salon', 'estado_salon')
    
    for reg in registros:
        estados_fecha[reg.salon_id] = {
            'codigo': reg.estado_salon.codigo,
            'nombre': reg.estado_salon.nombre
        }
    
    salones_data = []
    for salon in salones:
        esta_ocupado = salon.id in salon_ids_ocupados
        
        estado_data = estados_fecha.get(salon.id)
        
        if estado_data:
            estado_en_fecha = estado_data['nombre']
            codigo_estado = estado_data['codigo']
        else:
            estado_en_fecha = salon.estado_salon.nombre if salon.estado_salon else 'Disponible'
            codigo_estado = salon.estado_salon.codigo if salon.estado_salon else 'DIS'
        
        if esta_ocupado:
            estado_en_fecha = 'Ocupado'
            codigo_estado = 'OCUP'
        
        disponible = not esta_ocupado and codigo_estado in ['DIS', 'DISP']
        
        salones_data.append({
            'id': salon.id,
            'nombre': salon.nombre,
            'estado_salon': estado_en_fecha,
            'codigo_estado': codigo_estado,
            'reservado': esta_ocupado,
            'disponible': disponible,
            'max_capacidad': salon.maxCapacidad
        })
    
    return JsonResponse({
        'success': True,
        'salones': salones_data,
        'fecha': fecha_str
    })
