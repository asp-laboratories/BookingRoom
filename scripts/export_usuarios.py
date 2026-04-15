#!/usr/bin/env python
"""
Script para exportar datos de trabajadores, cuentas y clientes
desde la base de datos actual a la nueva base de datos
"""

import os
import sys
import django
import subprocess
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BookingRoom_Django.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

def main():
    print("=" * 70)
    print("EXPORTAR DATOS DE USUARIOS (Cuentas, Trabajadores, Clientes)")
    print("=" * 70)
    print()
    
    # Crear archivo de exportación con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archivo_export = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        f'export_usuarios_{timestamp}.sql'
    )
    
    print(f"Exportando datos desde 'bookingroom_test'...")
    print(f"Archivo de salida: {archivo_export}")
    print()
    
    # Comando pg_dump para tablas específicas
    tablas = [
        'rol',
        'estado_cuenta', 
        'tipo_cliente',
        'cuenta',
        'trabajador',
        'datos_cliente'
    ]
    
    try:
        # Exportar estructura + datos de las tablas necesarias
        cmd = [
            'pg_dump', '-U', 'postgres', '-d', 'bookingroom_test',
            '--format=plain',
            '--no-owner',
            '--no-acl',
            '--data-only',  # Solo datos, no estructura
            '--table=rol',
            '--table=estado_cuenta',
            '--table=tipo_cliente',
            '--table=cuenta',
            '--table=trabajador',
            '--table=datos_cliente'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, 'PGPASSWORD': 'postgres'})
        
        if result.returncode == 0:
            with open(archivo_export, 'w', encoding='utf-8') as f:
                f.write("-- ========================================\n")
                f.write("-- EXPORTACIÓN DE USUARIOS\n")
                f.write(f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-- ========================================\n\n")
                f.write("BEGIN;\n\n")
                f.write("-- Insertar con ON CONFLICT para evitar duplicados\n")
                f.write(result.stdout)
                f.write("\nCOMMIT;\n")
            
            # Contar registros exportados
            print("✅ Exportación exitosa!")
            print()
            
            # Contar registros
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM rol) as roles,
                        (SELECT COUNT(*) FROM estado_cuenta) as estados_cuenta,
                        (SELECT COUNT(*) FROM tipo_cliente) as tipos_cliente,
                        (SELECT COUNT(*) FROM cuenta) as cuentas,
                        (SELECT COUNT(*) FROM trabajador) as trabajadores,
                        (SELECT COUNT(*) FROM datos_cliente) as clientes
                """)
                row = cursor.fetchone()
                
            print("📊 Registros exportados:")
            print(f"   - Roles: {row[0]}")
            print(f"   - Estados de cuenta: {row[1]}")
            print(f"   - Tipos de cliente: {row[2]}")
            print(f"   - Cuentas: {row[3]}")
            print(f"   - Trabajadores: {row[4]}")
            print(f"   - Datos de clientes: {row[5]}")
            
            print(f"\n📁 Archivo: {archivo_export}")
            print(f"\n📝 Para importar en la nueva BD:")
            print(f"   psql -U postgres -d bookingroom_nuevadata -f {archivo_export}")
            
        else:
            print(f"❌ Error al exportar:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("❌ pg_dump no encontrado. Asegúrate de tener PostgreSQL instalado.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
