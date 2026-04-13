from django.http import JsonResponse
from django.db.models import Q
from BookingRoomApp import models
from datetime import datetime


def verificar_salon_disponible(request):
    """
    Verifica la disponibilidad de salones para una fecha específica.
    Similar a la lógica de Flutter: SalonService.getSalonesDisponibles()
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
    
    # Obtener todos los salones con su estado
    salones = models.Salon.objects.select_related('estado_salon').all()
    
    # Obtener reservaciones confirmadas para esa fecha
    reservaciones_fecha = models.Reservacion.objects.filter(
        fechaEvento=fecha_evento,
        estado_reserva__codigo__in=['CONF', 'CON']  # Confirmadas
    ).values_list('montaje__salon_id', flat=True)
    
    salones_data = []
    for salon in salones:
        # Verificar si el salón está reservado en esa fecha
        reservado = salon.id in reservaciones_fecha
        
        # Verificar si el estado del salón bloquea su uso
        estado_salon_nombre = salon.estado_salon.nombre if salon.estado_salon else ''
        
        salones_data.append({
            'id': salon.id,
            'nombre': salon.nombre,
            'estado_salon': estado_salon_nombre,
            'reservado': reservado,
            'disponible': not reservado and estado_salon_nombre not in ['Ocupado', 'Reservado', 'En Limpieza', 'Mantenimiento']
        })
    
    return JsonResponse({
        'success': True,
        'salones': salones_data,
        'fecha': fecha_str
    })
