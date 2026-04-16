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
        estado_reserva__codigo__in=['CONF', 'CON']
    ).values_list('montaje__salon_id', flat=True)
    
    # Obtener registros de estado de salon para esa fecha
    registros_estado = models.RegistrEstadSalon.objects.filter(
        fecha=fecha_evento
    ).values_list('salon_id', 'estado_salon__codigo', 'estado_salon__nombre')
    
    # Crear diccionario de estado por salon
    estado_salon_fecha = {}
    for salon_id, codigo, nombre in registros_estado:
        estado_salon_fecha[salon_id] = {'codigo': codigo, 'nombre': nombre}
    
    salones_data = []
    for salon in salones:
        # Verificar si el salón está reservado en esa fecha
        reservado = salon.id in reservaciones_fecha
        
        # Verificar estado del salón en la tabla registr_esta_salon
        registro_estado = estado_salon_fecha.get(salon.id, None)
        
        # Verificar si el estado del salón bloquea su uso
        estado_salon_nombre = salon.estado_salon.nombre if salon.estado_salon else ''
        
        # Si hay un registro de estado para esa fecha, usarlo
        if registro_estado:
            estado_en_fecha = registro_estado['nombre']
            codigo_estado = registro_estado['codigo']
        else:
            estado_en_fecha = estado_salon_nombre
            codigo_estado = salon.estado_salon.codigo if salon.estado_salon else ''
        
        # Disponible si: no reservado Y el estado no es de los bloqueados
        # Estados bloqueados: Reservado, Ocupado, En Limpieza, Mantenimiento (case-insensitive)
        estados_bloqueados = ['reservado', 'ocupado', 'en limpieza', 'mantenimiento']
        disponible = not reservado and estado_en_fecha.lower() not in estados_bloqueados and codigo_estado != 'OCUP'
        
        salones_data.append({
            'id': salon.id,
            'nombre': salon.nombre,
            'estado_salon': estado_en_fecha,
            'codigo_estado': codigo_estado,
            'reservado': reservado,
            'disponible': disponible,
            'max_capacidad': salon.maxCapacidad
        })
    
    return JsonResponse({
        'success': True,
        'salones': salones_data,
        'fecha': fecha_str
    })
