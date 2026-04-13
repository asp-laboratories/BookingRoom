from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import connection
from decimal import Decimal
from BookingRoomApp.views import get_cuenta_and_rol


def pagos(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "BookingRoomApp/recepcion/pagos.html", {"rol": rol})


def ejecutar_query(sql, params=None):
    """Ejecuta query SQL y retorna resultados como lista de dicts"""
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        columns = [col[0] for col in cursor.description]
        results = []
        for row in cursor.fetchall():
            row_dict = dict(zip(columns, row))
            # Convertir Decimal a float para JSON serialization
            for key, value in row_dict.items():
                if isinstance(value, Decimal):
                    row_dict[key] = float(value)
            results.append(row_dict)
        return results


def estadisticas(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))
    
    # ==========================================
    # EQUIPAMIENTO
    # ==========================================
    
    # Top 5 equipamiento mas requerido
    equipamiento_mas_requerido = ejecutar_query("""
        SELECT e.nombre, COUNT(re.id) as frecuencia
        FROM reserva_equipa re
        JOIN equipamiento e ON re.equipamiento_id = e.id
        GROUP BY e.id, e.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    # Dinero generado por equipamiento
    dinero_por_equipamiento = ejecutar_query("""
        SELECT e.nombre, SUM(e.costo * re.cantidad) as dinero_generado
        FROM reserva_equipa re
        JOIN equipamiento e ON re.equipamiento_id = e.id
        GROUP BY e.id, e.nombre
        ORDER BY dinero_generado DESC
        LIMIT 5
    """)
    
    # Equipamiento mas usado por tipo de evento
    equipamiento_por_tipo_evento = ejecutar_query("""
        SELECT te.nombre as tipo_evento, e.nombre as equipamiento, COUNT(re.id) as frecuencia
        FROM reserva_equipa re
        JOIN equipamiento e ON re.equipamiento_id = e.id
        JOIN reservacion r ON re.reservacion_id = r.id
        JOIN tipo_evento te ON r.tipo_evento_id = te.id
        GROUP BY te.nombre, e.id, e.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    # ==========================================
    # SERVICIOS
    # ==========================================
    
    # Top 5 servicios mas requeridos
    servicios_mas_requeridos = ejecutar_query("""
        SELECT s.nombre, COUNT(rs.id) as frecuencia
        FROM reserva_servicio rs
        JOIN servicio s ON rs.servicio_id = s.id
        GROUP BY s.id, s.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    # Dinero generado por servicios
    dinero_por_servicios = ejecutar_query("""
        SELECT s.nombre, SUM(s.costo) as dinero_generado
        FROM reserva_servicio rs
        JOIN servicio s ON rs.servicio_id = s.id
        GROUP BY s.id, s.nombre
        ORDER BY dinero_generado DESC
        LIMIT 5
    """)
    
    # Servicios mas usados por tipo de evento
    servicios_por_tipo_evento = ejecutar_query("""
        SELECT te.nombre as tipo_evento, s.nombre as servicio, COUNT(rs.id) as frecuencia
        FROM reserva_servicio rs
        JOIN servicio s ON rs.servicio_id = s.id
        JOIN reservacion r ON rs.reservacion_id = r.id
        JOIN tipo_evento te ON r.tipo_evento_id = te.id
        GROUP BY te.nombre, s.id, s.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    # ==========================================
    # MOBILIARIO
    # ==========================================
    
    # Top 5 mobiliario mas requerido
    mobiliario_mas_requerido = ejecutar_query("""
        SELECT m.nombre, COUNT(mm.id) as frecuencia
        FROM montaje_mobiliario mm
        JOIN mobiliario m ON mm.mobiliario_id = m.id
        GROUP BY m.id, m.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    # Dinero generado por mobiliario
    dinero_por_mobiliario = ejecutar_query("""
        SELECT m.nombre, SUM(m.costo * mm.cantidad) as dinero_generado
        FROM montaje_mobiliario mm
        JOIN mobiliario m ON mm.mobiliario_id = m.id
        GROUP BY m.id, m.nombre
        ORDER BY dinero_generado DESC
        LIMIT 5
    """)
    
    # Mobiliario mas usado por tipo de evento
    mobiliario_por_tipo_evento = ejecutar_query("""
        SELECT te.nombre as tipo_evento, m.nombre as mobiliario, COUNT(mm.id) as frecuencia
        FROM montaje_mobiliario mm
        JOIN mobiliario m ON mm.mobiliario_id = m.id
        JOIN montaje mt ON mm.montaje_id = mt.id
        JOIN reservacion r ON mt.id = r.montaje_id
        JOIN tipo_evento te ON r.tipo_evento_id = te.id
        GROUP BY te.nombre, m.id, m.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    # ==========================================
    # SALONES
    # ==========================================
    
    # Top 5 salones mas utilizados
    salones_mas_utilizados = ejecutar_query("""
        SELECT s.nombre, COUNT(r.id) as veces_utilizado
        FROM montaje m
        JOIN salon s ON m.salon_id = s.id
        JOIN reservacion r ON m.id = r.montaje_id
        GROUP BY s.id, s.nombre
        ORDER BY veces_utilizado DESC
        LIMIT 5
    """)
    
    # Dinero generado por salones
    dinero_por_salones = ejecutar_query("""
        SELECT s.nombre, SUM(s.costo) as dinero_generado
        FROM montaje m
        JOIN salon s ON m.salon_id = s.id
        JOIN reservacion r ON m.id = r.montaje_id
        GROUP BY s.id, s.nombre
        ORDER BY dinero_generado DESC
        LIMIT 5
    """)
    
    # Salones mas usados por tipo de evento
    salones_por_tipo_evento = ejecutar_query("""
        SELECT te.nombre as tipo_evento, s.nombre as salon, COUNT(r.id) as frecuencia
        FROM montaje m
        JOIN salon s ON m.salon_id = s.id
        JOIN reservacion r ON m.id = r.montaje_id
        JOIN tipo_evento te ON r.tipo_evento_id = te.id
        GROUP BY te.nombre, s.id, s.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    # ==========================================
    # TIPOS DE MONTAJE
    # ==========================================
    
    # Top 5 tipos de montaje mas usados
    tipos_montaje_mas_usados = ejecutar_query("""
        SELECT tm.nombre, COUNT(m.id) as frecuencia
        FROM montaje m
        JOIN tipo_montaje tm ON m.tipo_montaje_id = tm.id
        JOIN reservacion r ON m.id = r.montaje_id
        GROUP BY tm.id, tm.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    # Tipos de montaje mas usados por tipo de evento
    montajes_por_tipo_evento = ejecutar_query("""
        SELECT te.nombre as tipo_evento, tm.nombre as montaje, COUNT(m.id) as frecuencia
        FROM montaje m
        JOIN tipo_montaje tm ON m.tipo_montaje_id = tm.id
        JOIN reservacion r ON m.id = r.montaje_id
        JOIN tipo_evento te ON r.tipo_evento_id = te.id
        GROUP BY te.nombre, tm.id, tm.nombre
        ORDER BY frecuencia DESC
        LIMIT 5
    """)
    
    context = {
        "rol": rol,
        # Equipamiento
        "equipamiento_mas_requerido": equipamiento_mas_requerido,
        "dinero_por_equipamiento": dinero_por_equipamiento,
        "equipamiento_por_tipo_evento": equipamiento_por_tipo_evento,
        # Servicios
        "servicios_mas_requeridos": servicios_mas_requeridos,
        "dinero_por_servicios": dinero_por_servicios,
        "servicios_por_tipo_evento": servicios_por_tipo_evento,
        # Mobiliario
        "mobiliario_mas_requerido": mobiliario_mas_requerido,
        "dinero_por_mobiliario": dinero_por_mobiliario,
        "mobiliario_por_tipo_evento": mobiliario_por_tipo_evento,
        # Salones
        "salones_mas_utilizados": salones_mas_utilizados,
        "dinero_por_salones": dinero_por_salones,
        "salones_por_tipo_evento": salones_por_tipo_evento,
        # Tipos de montaje
        "tipos_montaje_mas_usados": tipos_montaje_mas_usados,
        "montajes_por_tipo_evento": montajes_por_tipo_evento,
    }
    
    return render(request, "BookingRoomApp/administracion/estadisticas.html", context)


def historial_reservacion(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'BookingRoomApp/recepcion/historial_reservacion.html', {'rol': rol})