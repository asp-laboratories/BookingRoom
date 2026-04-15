#!/usr/bin/env python
"""
Script de backup selectivo para BookingRoom
Guarda datos fundamentales antes de hacer limpieza de datos basura
"""

import os
import sys
import json
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookingRoom_Django.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from BookingRoomApp import models
from django.core.serializers import serialize
from django.db import connection

def ejecutar_query(sql):
    """Ejecuta query SQL y retorna resultados"""
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def backup_tabla(nombre_tabla, archivo):
    """Backup de una tabla específica"""
    try:
        datos = ejecutar_query(f'SELECT * FROM {nombre_tabla}')
        archivo.write(f"\n-- ========================================\n")
        archivo.write(f"-- Backup de tabla: {nombre_tabla}\n")
        archivo.write(f"-- Total registros: {len(datos)}\n")
        archivo.write(f"-- ========================================\n\n")
        
        if not datos:
            archivo.write(f"-- Tabla vacía\n\n")
            return len(datos)
        
        for row in datos:
            archivo.write(f"INSERT INTO {nombre_tabla} (")
            columns = ', '.join(row.keys())
            archivo.write(f"{columns}) VALUES (")
            
            values = []
            for key, value in row.items():
                if value is None:
                    values.append('NULL')
                elif isinstance(value, str):
                    values.append("'" + value.replace("'", "''") + "'")
                elif isinstance(value, bool):
                    values.append('TRUE' if value else 'FALSE')
                else:
                    values.append(str(value))
            
            archivo.write(', '.join(values))
            archivo.write(');\n')
        
        archivo.write('\n')
        return len(datos)
        
    except Exception as e:
        archivo.write(f"-- ERROR al hacer backup de {nombre_tabla}: {str(e)}\n\n")
        return 0

def main():
    print("=" * 70)
    print("BACKUP SELECTIVO DE BOOKINGROOM")
    print("=" * 70)
    print()
    
    # Crear archivo de backup con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo_backup = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        f'backup_completo_{timestamp}.sql'
    )
    
    print(f"Creando backup en: {archivo_backup}\n")
    
    with open(archivo_backup, 'w', encoding='utf-8') as f:
        # Header
        f.write("-- ========================================\n")
        f.write("-- BACKUP SELECTIVO BOOKINGROOM\n")
        f.write(f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-- ========================================\n\n")
        f.write("BEGIN;\n\n")
        
        total_registros = 0
        
        # ========================================
        # 1. TABLAS DE CATÁLOGO Y ESTADO
        # ========================================
        print("📦 Respaldando tablas de catálogo y estado...")
        
        catalogos = [
            ('rol', 'Roles'),
            ('estado_cuenta', 'Estados de cuenta'),
            ('tipo_cliente', 'Tipos de cliente'),
            ('estado_mobil', 'Estados de mobiliario'),
            ('caracter_mobi', 'Características de mobiliario'),
            ('tipo_mobil', 'Tipos de mobiliario'),
            ('tipo_montaje', 'Tipos de montaje'),
            ('tipo_evento', 'Tipos de evento'),
            ('estado_reserva', 'Estados de reservación'),
            ('estado_salon', 'Estados de salón'),
            ('tipo_equipa', 'Tipos de equipamiento'),
            ('estado_equipa', 'Estados de equipamiento'),
            ('concepto_pago', 'Conceptos de pago'),
            ('metodo_pago', 'Métodos de pago'),
            ('tipo_servicio', 'Tipos de servicio'),
        ]
        
        for tabla, nombre in catalogos:
            count = backup_tabla(tabla, f)
            print(f"  ✅ {nombre} ({tabla}): {count} registros")
            total_registros += count
        
        # ========================================
        # 2. CUENTAS Y USUARIOS
        # ========================================
        print("\n📦 Respaldando cuentas y usuarios...")
        
        cuentas = [
            ('cuenta', 'Cuentas'),
            ('trabajador', 'Trabajadores'),
            ('datos_cliente', 'Datos de clientes'),
        ]
        
        for tabla, nombre in cuentas:
            count = backup_tabla(tabla, f)
            print(f"  ✅ {nombre} ({tabla}): {count} registros")
            total_registros += count
        
        # ========================================
        # 3. SERVICIOS Y ACTIVOS
        # ========================================
        print("\n📦 Respaldando servicios y activos...")
        
        servicios = [
            ('servicio', 'Servicios'),
            ('equipamiento', 'Equipamiento'),
            ('mobiliario', 'Mobiliario'),
            ('salon', 'Salones'),
        ]
        
        for tabla, nombre in servicios:
            count = backup_tabla(tabla, f)
            print(f"  ✅ {nombre} ({tabla}): {count} registros")
            total_registros += count
        
        # ========================================
        # 4. INVENTARIOS (si hay datos útiles)
        # ========================================
        print("\n📦 Respaldando inventarios...")
        
        inventarios = [
            ('inventario_mobil', 'Inventario mobiliario'),
            ('inventario_equipa', 'Inventario equipamiento'),
        ]
        
        for tabla, nombre in inventarios:
            count = backup_tabla(tabla, f)
            print(f"  ✅ {nombre} ({tabla}): {count} registros")
            total_registros += count
        
        # Commit final
        f.write("\nCOMMIT;\n")
        f.write("\n-- ========================================\n")
        f.write(f"-- BACKUP COMPLETADO\n")
        f.write(f"-- Total de registros respaldados: {total_registros}\n")
        f.write(f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-- ========================================\n")
    
    print("\n" + "=" * 70)
    print(f"✅ BACKUP COMPLETADO")
    print(f"📁 Archivo: {archivo_backup}")
    print(f"📊 Total registros respaldados: {total_registros}")
    print("=" * 70)
    print("\n📝 Para restaurar después de la limpieza:")
    print(f"   psql -U postgres -d bookingroom_test -f {archivo_backup}")
    print("\n⚠️  IMPORTANTE:")
    print("   - Este backup NO incluye reservaciones, pagos ni montajes")
    print("   - Si necesitas esos datos, haz un pg_dump completo primero")
    print("   - Cambiar CASCADE eliminará datos en cascada, ¡ten cuidado!")
    print("=" * 70)

if __name__ == '__main__':
    main()
