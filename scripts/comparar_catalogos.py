#!/usr/bin/env python
"""
Script de comparación entre backup actual y nuevo SQL de prueba
Identifica diferencias en catálogos para evitar problemas
"""

import os
import sys

# Colores para terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def comparar_catalogos():
    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}  COMPARACIÓN DE CATÁLOGOS: Backup vs Nuevo SQL{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    # ========================================
    # 1. ROLES
    # ========================================
    print(f"{YELLOW}📦 1. ROLES{RESET}")
    print("-" * 60)
    
    backup_roles = {
        'ADMIN': 'Administrador',
        'COORD': 'Coordinador',
        'RECEP': 'Recepcionista',
        'ALMAC': 'Almacen',
    }
    
    nuevo_roles = {
        'ADMIN': 'Administrador',
        'RECEP': 'Recepcionista',
        'COORD': 'Coordinador',
        'ALM': 'Almacenista',  # ⚠️ DIFERENTE!
    }
    
    print(f"  Backup: {len(backup_roles)} roles")
    print(f"  Nuevo:  {len(nuevo_roles)} roles")
    
    # Comparar
    for codigo in set(list(backup_roles.keys()) + list(nuevo_roles.keys())):
        backup_nombre = backup_roles.get(codigo)
        nuevo_nombre = nuevo_roles.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre != nuevo_nombre:
                print(f"  {RED}❌ '{codigo}': '{backup_nombre}' → '{nuevo_nombre}'{RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 2. ESTADOS DE CUENTA
    # ========================================
    print(f"{YELLOW}📦 2. ESTADOS DE CUENTA{RESET}")
    print("-" * 60)
    
    backup_ec = {
        'ACT': 'Activa',
        'SUSPE': 'Suspendida',
        'BANEO': 'Bloqueada',
    }
    
    nuevo_ec = {
        'ACT': 'Activa',
        'SUSP': 'Suspendida',  # ⚠️ DIFERENTE!
        'INACT': 'Inactiva',    # ⚠️ DIFERENTE!
    }
    
    print(f"  Backup: {len(backup_ec)} estados")
    print(f"  Nuevo:  {len(nuevo_ec)} estados")
    
    for codigo in set(list(backup_ec.keys()) + list(nuevo_ec.keys())):
        backup_nombre = backup_ec.get(codigo)
        nuevo_nombre = nuevo_ec.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre != nuevo_nombre:
                print(f"  {RED}❌ '{codigo}': '{backup_nombre}' → '{nuevo_nombre}'{RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 3. TIPOS DE CLIENTE
    # ========================================
    print(f"{YELLOW}📦 3. TIPOS DE CLIENTE{RESET}")
    print("-" * 60)
    
    backup_tc = {
        'MOR': 'Persona moral',
        'FIS': 'Persona fisica',
        'PM': 'Persona Moral',
        'PF': 'Persona Fisica',
    }
    
    nuevo_tc = {
        'FIS': 'Persona Física',
        'MOR': 'Persona Moral',
        'EXT': 'Extranjero',
        'GOB': 'Gobierno',
    }
    
    print(f"  Backup: {len(backup_tc)} tipos")
    print(f"  Nuevo:  {len(nuevo_tc)} tipos")
    
    for codigo in set(list(backup_tc.keys()) + list(nuevo_tc.keys())):
        backup_nombre = backup_tc.get(codigo)
        nuevo_nombre = nuevo_tc.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' → '{nuevo_nombre}' (difiere){RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 4. ESTADOS DE MOBILIARIO
    # ========================================
    print(f"{YELLOW}📦 4. ESTADOS DE MOBILIARIO{RESET}")
    print("-" * 60)
    
    backup_em = {
        'DISP': 'Disponible',
        'OCUP': 'Ocupado',
        'RESV': 'Reservado',
        'REPAR': 'En reparacion',
    }
    
    nuevo_em = {
        'DISP': 'Disponible',
        'OCUP': 'Ocupado',
        'DAN': 'Dañado',
        'MAN': 'En Mantenimiento',
    }
    
    print(f"  Backup: {len(backup_em)} estados")
    print(f"  Nuevo:  {len(nuevo_em)} estados")
    
    for codigo in set(list(backup_em.keys()) + list(nuevo_em.keys())):
        backup_nombre = backup_em.get(codigo)
        nuevo_nombre = nuevo_em.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' → '{nuevo_nombre}' (difiere){RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 5. TIPOS DE MONTAJE
    # ========================================
    print(f"{YELLOW}📦 5. TIPOS DE MONTAJE{RESET}")
    print("-" * 60)
    
    backup_tm = {
        1: 'Teatro',
        2: 'Escuela',
        3: 'Banquete',
        4: 'Recepcion',
        5: 'Imperial',
        6: 'Herradura',
        7: 'Mesa rusa',
    }
    
    nuevo_tm = {
        1: 'Auditorio/Teatro',
        2: 'Escuela/Aula',
        3: 'Herradura/U',
        4: 'Imperial',
        5: 'Banquete',
        6: 'Cóctel/Recepción',
        7: 'Mesa Redonda',
        8: 'Estilo Lounge',
        9: 'Mesa Rusa/O',
        10: 'Española/Boardroom',
    }
    
    print(f"  Backup: {len(backup_tm)} tipos")
    print(f"  Nuevo:  {len(nuevo_tm)} tipos")
    
    for id_tipo in set(list(backup_tm.keys()) + list(nuevo_tm.keys())):
        backup_nombre = backup_tm.get(id_tipo)
        nuevo_nombre = nuevo_tm.get(id_tipo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  ID {id_tipo}: '{backup_nombre}' → '{nuevo_nombre}' (cambia){RESET}")
            else:
                print(f"  {GREEN}✅ ID {id_tipo}: {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  ID {id_tipo}: '{backup_nombre}' - ELIMINADO{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ ID {id_tipo}: '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 6. ESTADOS DE RESERVACIÓN
    # ========================================
    print(f"{YELLOW}📦 6. ESTADOS DE RESERVACIÓN{RESET}")
    print("-" * 60)
    
    backup_er = {
        'SOLIC': 'Solicitada',
        'PEN': 'Pendiente',
        'CONF': 'Confirmada',
        'CON': 'Confirmada',
        'ENPRO': 'En proceso',
        'FIN': 'Finalizada',
        'CAN': 'Cancelada',
        'PAGAD': 'Pagada',
        'PLANT': 'Plantilla',
    }
    
    nuevo_er = {
        'SOLIC': 'Solicitada',
        'PEN': 'Pendiente',
        'CON': 'Confirmada',
        'ENPRO': 'En Proceso',
        'PAGAD': 'Pagada',
        'FIN': 'Finalizada',
        'CAN': 'Cancelada',
        'CANC': 'Cancelada por Cliente',
        'RECH': 'Rechazada',
    }
    
    print(f"  Backup: {len(backup_er)} estados")
    print(f"  Nuevo:  {len(nuevo_er)} estados")
    
    for codigo in set(list(backup_er.keys()) + list(nuevo_er.keys())):
        backup_nombre = backup_er.get(codigo)
        nuevo_nombre = nuevo_er.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' → '{nuevo_nombre}' (difiere){RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 7. ESTADOS DE SALÓN
    # ========================================
    print(f"{YELLOW}📦 7. ESTADOS DE SALÓN{RESET}")
    print("-" * 60)
    
    backup_es = {
        'DIS': 'Disponible',
        'RESV': 'Reservado',
        'OCUP': 'Ocupado',
        'MANTE': 'En mantenimiento',
        'LIMPI': 'En limpieza',
    }
    
    nuevo_es = {
        'DIS': 'Disponible',
        'OCUP': 'Ocupado',
        'RESV': 'Reservado',
        'LIMP': 'En Limpieza',
        'MAN': 'En Mantenimiento',
    }
    
    print(f"  Backup: {len(backup_es)} estados")
    print(f"  Nuevo:  {len(nuevo_es)} estados")
    
    for codigo in set(list(backup_es.keys()) + list(nuevo_es.keys())):
        backup_nombre = backup_es.get(codigo)
        nuevo_nombre = nuevo_es.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' → '{nuevo_nombre}' (difiere){RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 8. TIPOS DE EQUIPAMIENTO
    # ========================================
    print(f"{YELLOW}📦 8. TIPOS DE EQUIPAMIENTO{RESET}")
    print("-" * 60)
    
    backup_te = {
        1: 'Audio',
        2: 'Video',
        3: 'Iluminacion',
        4: 'Computo',
        5: 'Mobiliario extra',
        6: 'Otro',
    }
    
    nuevo_te = {
        1: 'Audio',
        2: 'Video/Proyección',
        3: 'Iluminación',
        4: 'Climatización',
        5: 'Equipos para reuniones',
        6: 'Equipo empresarial',
        7: 'Telecomunicaciones',
        8: 'Accesorios de presentación',
    }
    
    print(f"  Backup: {len(backup_te)} tipos")
    print(f"  Nuevo:  {len(nuevo_te)} tipos")
    
    for id_tipo in set(list(backup_te.keys()) + list(nuevo_te.keys())):
        backup_nombre = backup_te.get(id_tipo)
        nuevo_nombre = nuevo_te.get(id_tipo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  ID {id_tipo}: '{backup_nombre}' → '{nuevo_nombre}' (cambia){RESET}")
            else:
                print(f"  {GREEN}✅ ID {id_tipo}: {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  ID {id_tipo}: '{backup_nombre}' - ELIMINADO{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ ID {id_tipo}: '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 9. ESTADOS DE EQUIPAMIENTO
    # ========================================
    print(f"{YELLOW}📦 9. ESTADOS DE EQUIPAMIENTO{RESET}")
    print("-" * 60)
    
    backup_ee = {
        'DISP': 'Disponible',
        'FUNC': 'Funcional',
        'DANAD': 'Daniado',
        'REPAR': 'En reparacion',
        'RESV': 'Reservado',
    }
    
    nuevo_ee = {
        'DISP': 'Disponible',
        'OCUP': 'Ocupado',
        'DAN': 'Dañado',
        'MAN': 'En Mantenimiento',
        'RESV': 'Reservado',
    }
    
    print(f"  Backup: {len(backup_ee)} estados")
    print(f"  Nuevo:  {len(nuevo_ee)} estados")
    
    for codigo in set(list(backup_ee.keys()) + list(nuevo_ee.keys())):
        backup_nombre = backup_ee.get(codigo)
        nuevo_nombre = nuevo_ee.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' → '{nuevo_nombre}' (difiere){RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 10. CONCEPTOS DE PAGO
    # ========================================
    print(f"{YELLOW}📦 10. CONCEPTOS DE PAGO{RESET}")
    print("-" * 60)
    
    backup_cp = {
        'ANTIC': 'Anticipo',
        'LIQUI': 'Liquidacion',
        'EXTR': 'Extra',
        'ABONO': 'Abono',
        'PENAL': 'Penalizacion',
    }
    
    nuevo_cp = {
        'ABON': 'Abono',
        'LIQ': 'Liquidación',
        'EXT': 'Extra',
        'CANC': 'Cancelación',
        'ADIC': 'Adicional',
    }
    
    print(f"  Backup: {len(backup_cp)} conceptos")
    print(f"  Nuevo:  {len(nuevo_cp)} conceptos")
    
    for codigo in set(list(backup_cp.keys()) + list(nuevo_cp.keys())):
        backup_nombre = backup_cp.get(codigo)
        nuevo_nombre = nuevo_cp.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' → '{nuevo_nombre}' (difiere){RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 11. MÉTODOS DE PAGO
    # ========================================
    print(f"{YELLOW}📦 11. MÉTODOS DE PAGO{RESET}")
    print("-" * 60)
    
    backup_mp = {
        'EFECT': 'Efectivo',
        'TRANS': 'Transferencia',
        'TARJE': 'Tarjeta',
        'NFC': 'NFC',
        'CHEQU': 'Cheque',
    }
    
    nuevo_mp = {
        'EFEC': 'Efectivo',
        'TARJ': 'Tarjeta de Crédito',
        'NFC': 'Contactless/NFC',
        'TRANS': 'Transferencia',
        'CHEQ': 'Cheque',
    }
    
    print(f"  Backup: {len(backup_mp)} métodos")
    print(f"  Nuevo:  {len(nuevo_mp)} métodos")
    
    for codigo in set(list(backup_mp.keys()) + list(nuevo_mp.keys())):
        backup_nombre = backup_mp.get(codigo)
        nuevo_nombre = nuevo_mp.get(codigo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' → '{nuevo_nombre}' (difiere){RESET}")
            else:
                print(f"  {GREEN}✅ '{codigo}': {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  '{codigo}': '{backup_nombre}' - ELIMINADO en nuevo{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ '{codigo}': '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # 12. TIPOS DE SERVICIO
    # ========================================
    print(f"{YELLOW}📦 12. TIPOS DE SERVICIO{RESET}")
    print("-" * 60)
    
    backup_ts = {
        1: 'Catering',
        2: 'Audiovisual',
        3: 'Decoracion',
        4: 'Transporte',
        5: 'Fotografia',
        6: 'Musica',
        7: 'Seguridad',
        8: 'Limpieza',
        9: 'Otro',
        10: 'Internet',
    }
    
    nuevo_ts = {
        1: 'Servicios para reuniones',
        2: 'Servicios ejecutivos',
        3: 'Internet y Telecom',
        4: 'Catering y Alimentos',
        5: 'Decoración y Ambientación',
        6: 'Logística y Coordinación',
        7: 'Audiovisuales',
        8: 'Limpieza y Mantenimiento',
        9: 'Seguridad',
        10: 'Transporte',
    }
    
    print(f"  Backup: {len(backup_ts)} tipos")
    print(f"  Nuevo:  {len(nuevo_ts)} tipos")
    
    for id_tipo in set(list(backup_ts.keys()) + list(nuevo_ts.keys())):
        backup_nombre = backup_ts.get(id_tipo)
        nuevo_nombre = nuevo_ts.get(id_tipo)
        
        if backup_nombre and nuevo_nombre:
            if backup_nombre.lower() != nuevo_nombre.lower():
                print(f"  {YELLOW}⚠️  ID {id_tipo}: '{backup_nombre}' → '{nuevo_nombre}' (CAMBIA){RESET}")
            else:
                print(f"  {GREEN}✅ ID {id_tipo}: {backup_nombre}{RESET}")
        elif backup_nombre and not nuevo_nombre:
            print(f"  {YELLOW}⚠️  ID {id_tipo}: '{backup_nombre}' - ELIMINADO{RESET}")
        elif not backup_nombre and nuevo_nombre:
            print(f"  {GREEN}➕ ID {id_tipo}: '{nuevo_nombre}' - NUEVO{RESET}")
    
    print()
    
    # ========================================
    # RESUMEN FINAL
    # ========================================
    print(f"{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}  RESUMEN DE COMPARACIÓN{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")
    
    print(f"{YELLOW}⚠️  PROBLEMAS DETECTADOS:{RESET}")
    print(f"  1. {RED}ROLES: 'ALMAC' → 'ALM' (cambia código){RESET}")
    print(f"  2. {RED}ESTADO_CUENTA: 'SUSPE' → 'SUSP', 'BANEO' → 'INACT'{RESET}")
    print(f"  3. {RED}ESTADO_MOBILIARIO: 'RESV' → 'DAN', 'REPAR' → 'MAN'{RESET}")
    print(f"  4. {RED}ESTADO_EQUIPAMIENTO: 'FUNC' → 'OCUP', 'DANAD' → 'DAN', 'REPAR' → 'MAN'{RESET}")
    print(f"  5. {RED}ESTADO_SALON: 'MANTE' → 'MAN', 'LIMPI' → 'LIMP'{RESET}")
    print(f"  6. {RED}CONCEPTO_PAGO: 'ANTIC' → 'ABON', 'LIQUI' → 'LIQ', etc.{RESET}")
    print(f"  7. {RED}METODO_PAGO: 'EFECT' → 'EFEC', 'TARJE' → 'TARJ', 'CHEQU' → 'CHEQ'{RESET}")
    print(f"  8. {YELLOW}TIPOS_SERVICIO: Todos los nombres cambian (pero ID se mantiene){RESET}")
    print(f"  9. {YELLOW}TIPOS_MONTAJE: Todos los nombres cambian (pero ID se mantiene){RESET}")
    
    print(f"\n{GREEN}✅ LO QUE SE MANTIENE:{RESET}")
    print(f"  - TIPO_CLIENTE: 'FIS' y 'MOR' se mantienen")
    print(f"  - TIPO_EVENTO: Se mantienen los 11 existentes + nuevos")
    print(f"  - ESTADO_RESERVA: 'SOLIC', 'PEN', 'CON', 'ENPRO', 'FIN', 'CAN', 'PAGAD' se mantienen")
    
    print(f"\n{YELLOW}⚠️  RECOMENDACIÓN:{RESET}")
    print(f"  Para evitar problemas, el nuevo SQL debe USAR LOS MISMOS CÓDIGOS")
    print(f"  que ya existen en la base de datos actual. Los nombres pueden cambiar,")
    print(f"  pero los códigos (PRIMARY KEY) deben ser idénticos para evitar")
    print(f"  errores de integridad referencial.\n")

if __name__ == '__main__':
    comparar_catalogos()
