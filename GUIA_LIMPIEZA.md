# 🗑️ Guía de Limpieza Segura de Base de Datos

## ✅ Backups Creados

| Archivo | Qué contiene | Cuándo usar |
|---------|-------------|-------------|
| `backup_completo_db_*.sql` | **BASE DE DATOS COMPLETA** | Si todo sale mal, restaura todo |
| `backup_completo_*.sql` | Solo catálogos y datos importantes | Para restaurar datos fundamentales |

## 📦 Datos Respaldados (221 registros)

### Catálogos y Estados (74 registros)
- ✅ Roles: 4
- ✅ Estados de cuenta: 3
- ✅ Tipos de cliente: 4
- ✅ Estados de mobiliario: 4
- ✅ Tipos de mobiliario: 5
- ✅ Tipos de montaje: 7
- ✅ Tipos de evento: 11
- ✅ Estados de reservación: 9
- ✅ Estados de salón: 5
- ✅ Tipos de equipamiento: 6
- ✅ Estados de equipamiento: 5
- ✅ Conceptos de pago: 5
- ✅ Métodos de pago: 5
- ✅ Tipos de servicio: 10

### Cuentas y Usuarios (25 registros)
- ✅ Cuentas: 14
- ✅ Trabajadores: 5
- ✅ Datos de clientes: 6

### Servicios y Activos (51 registros)
- ✅ Servicios: 16
- ✅ Equipamiento: 14
- ✅ Mobiliario: 10
- ✅ Salones: 11

### Inventarios (61 registros)
- ✅ Inventario mobiliario: 22
- ✅ Inventario equipamiento: 39

## ⚠️ CASCADE: Qué Pasará

### Modelos con `on_delete=models.CASCADE`:

| Modelo | Campo CASCADE | Si eliminas X, también se elimina |
|--------|--------------|----------------------------------|
| `Trabajador` | `cuenta` | ✅ Trabajador si eliminas Cuenta |
| `DatosCliente` | `cuenta` | ✅ DatosCliente si eliminas Cuenta |
| `Reservacion` | `cliente`, `montaje`, `estado_reserva`, `tipo_evento`, `trabajador` | ✅ Reservación si eliminas cualquiera |
| `Montaje` | `salon`, `tipo_montaje` | ✅ Montaje si eliminas Salón o TipoMontaje |
| `MontajeMobiliario` | `montaje`, `mobiliario` | ✅ Si eliminas Montaje o Mobiliario |
| `ReservaServicio` | `reservacion`, `servicio` | ✅ Si eliminas Reservación o Servicio |
| `ReservaEquipa` | `reservacion`, `equipamiento` | ✅ Si eliminas Reservación o Equipamiento |
| `RegistrEstadReserva` | `reservacion`, `estado_reserva` | ✅ Si eliminas Reservación o Estado |
| `RegistrEstadSalon` | `salon`, `estado_salon` | ✅ Si eliminas Salón o Estado |
| `InventarioMob` | `mobiliario`, `estado_mobil` | ✅ Si eliminas Mobiliario o Estado |
| `InventarioEquipa` | `equipamiento`, `estado_equipa` | ✅ Si eliminas Equipamiento o Estado |
| `Pago` | `reservacion`, `concepto_pago`, `metodo_pago` | ✅ Si eliminas Reservación |

### Modelos con `on_delete=models.PROTECT`:
Estos **NO te dejarán eliminar** si tienen registros relacionados:
- ✅ `Servicio.tipo_servicio`
- ✅ `Trabajador.rol`
- ✅ `Cuenta.estado_cuenta`
- ✅ `DatosCliente.tipo_cliente`
- ✅ `Salon.estado_salon`
- ✅ `Montaje.salon`, `Montaje.tipo_montaje`
- ✅ Y muchos más...

## 🧹 Estrategia de Limpieza Segura

### Opción 1: Solo eliminar datos basura (Recomendada)
```python
# Ejemplo en Django shell
from BookingRoomApp import models

# Eliminar solo reservaciones de prueba
models.Reservacion.objects.filter(nombreEvento__icontains='prueba').delete()

# Eliminar clientes de prueba
models.DatosCliente.objects.filter(nombre__icontains='prueba').delete()

# Eliminar cuentas de prueba
models.Cuenta.objects.filter(nombre_usuario__startswith='test').delete()
```

### Opción 2: Truncate con precaución
```sql
-- Eliminar SOLO datos de transacciones (no catálogos)
TRUNCATE TABLE pago CASCADE;
TRUNCATE TABLE reserva_servicio CASCADE;
TRUNCATE TABLE reserva_equipa CASCADE;
TRUNCATE TABLE montaje_mobiliario CASCADE;
TRUNCATE TABLE montaje CASCADE;
TRUNCATE TABLE reservacion CASCADE;
TRUNCATE TABLE registr_esta_reserva CASCADE;
TRUNCATE TABLE registr_esta_salon CASCADE;
TRUNCATE TABLE encuesta CASCADE;
```

### Opción 3: Drop y recrear (Nuclear)
```bash
# Eliminar toda la base de datos
dropdb -U postgres bookingroom_test

# Recrear
createdb -U postgres bookingroom_test

# Aplicar migraciones
python manage.py migrate

# Restaurar backups
psql -U postgres -d bookingroom_test -f backup_completo_20260414_054151.sql
```

## 📊 Para Ver Datos Antes de Eliminar

```sql
-- Ver reservaciones de prueba
SELECT id, "nombreEvento", estado_reserva_id 
FROM reservacion 
WHERE "nombreEvento" ILIKE '%prueba%' 
   OR "nombreEvento" ILIKE '%test%';

-- Ver clientes de prueba
SELECT id, nombre, rfc 
FROM datos_cliente 
WHERE nombre ILIKE '%prueba%' 
   OR nombre ILIKE '%test%';

-- Ver cuentas de prueba
SELECT id, nombre_usuario, correo_electronico 
FROM cuenta 
WHERE nombre_usuario ILIKE '%test%';

-- Contar registros por tabla
SELECT 'reservacion' as tabla, COUNT(*) FROM reservacion
UNION ALL
SELECT 'pago', COUNT(*) FROM pago
UNION ALL
SELECT 'datos_cliente', COUNT(*) FROM datos_cliente
UNION ALL
SELECT 'cuenta', COUNT(*) FROM cuenta;
```

## 🔄 Para Restaurar Después

### Restaurar backup completo:
```bash
psql -U postgres -d bookingroom_test -f backup_completo_db_20260413_224213.sql
```

### Restaurar solo catálogos y datos importantes:
```bash
psql -U postgres -d bookingroom_test -f backup_completo_20260414_054151.sql
```

## ⚠️ ADVERTENCIAS

1. **CASCADE eliminará en cascada**: Si eliminas un catálogo, se eliminarán todos los registros relacionados
2. **Backup completo ANTES de hacer cualquier cambio**
3. **Prueba en una BD de prueba primero**
4. **No elimines catálogos a menos que estés 100% seguro**

## 📋 Checklist Antes de Limpiar

- [ ] Backup completo creado ✅ (`backup_completo_db_*.sql`)
- [ ] Backup selectivo creado ✅ (`backup_completo_*.sql`)
- [ ] Identificados los datos basura
- [ ] Decidida la estrategia de limpieza
- [ ] Probado en entorno de desarrollo
- [ ] Listo para restaurar si algo sale mal
