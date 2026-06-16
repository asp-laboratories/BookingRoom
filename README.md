<h1 align="center">BookingRoom - Sistema de Gestión de Eventos en Hoteles</h1>

<p align="center">
  <img src="../../BookingRoom.png" alt="BookingRoom" width="360"/>
</p>
---

<p align="center">
  <img src="../../Presentacion(1).gif" alt="Presentación del sistema"/>
</p>

## Tabla de contenidos

- [Descripción y contexto](#descripción-y-contexto)
- [Guía de usuario](#guía-de-usuario)
- [Guía de instalación](#guía-de-instalación)
- [Cómo contribuir](#cómo-contribuir)
- [Autor/es](#autores)
- [Información adicional](#información-adicional)
- [Limitaciones del sistema](#limitaciones-del-sistema)

## Descripción y contexto

Sistema web para la gestión y administración de eventos en salones de un hotel.

**BookingRoom** — la palabra *gestión* proviene de la acción que se realiza al llevar el manejo del mobiliario y equipamiento para una mejor organización. Nuestro sistema está comprometido a tomar estos procesos para hacerlos más fáciles. Por otra parte, la palabra *administración* está establecida porque este sistema está fuertemente ligado a procesos como reservaciones y pagos. BookingRoom son dos palabras en inglés cuyo significado se basa en *reservar un salón*.

La función principal del sistema es la **reservación**. Será capaz de atender las solicitudes de los clientes que requieran reservar un salón, al igual que registrar reservaciones en caso de ser presencial. La reservación es el eje central del sistema; mediante una reservación se ejecutarán una serie de acciones en las cuales distintas áreas son partícipes para lograr efectuar la realización del evento.

## Guía de usuario

Las funcionalidades del sistema están divididas entre 4 roles: **administrador**, **recepcionista**, **almacenista** y **cliente**.

### 1. Administrador (Control Total y Gestión de Catálogos)

El Administrador tiene control total sobre la configuración del sistema, la infraestructura del hotel y la gestión del personal.

**Funcionalidades principales:**

- **Gestión de Personal:** Registrar nuevos trabajadores (RFC, número de empleado, nombre, correo y teléfono), consultar, modificar, asignar roles (recepcionista, almacenista o administrador) y realizar bajas lógicas.
- **Gestión de Clientes:** Habilitar o deshabilitar cuentas de cliente (Activo/Inactivo).
- **Catálogo de Salones:** Registrar infraestructura (nombre, dimensiones en m², ubicación y tarifa), modificar atributos y cambiar estado operativo (Disponible, Reservado, En Mantenimiento, Inactivo).
- **Catálogo de Servicios, Equipamiento y Mobiliario:** Crear, consultar, modificar y deshabilitar categorías y elementos del inventario técnico y servicios complementarios.

**Pasos básicos:**

1. Inicie sesión con su usuario y contraseña. El sistema lo redireccionará al Panel de Control con acceso a todas las pestañas.
2. Diríjase a *Catálogos* → *Salones* o *Servicios*. Haga clic en "Registrar", complete el formulario y confirme.
3. Para administrar personal, vaya a *Usuarios* → *Trabajadores*, busque por número de registro y modifique Rol o Estado.

### 2. Recepcionista (Atención al Cliente, Reservaciones y Pagos)

El personal de recepción se encarga de la interacción directa con el cliente, el control de la agenda y el seguimiento financiero.

**Funcionalidades principales:**

- **Gestión de Reservaciones:** Registrar, consultar y modificar reservaciones en una agenda digital integrada.
- **Captura de Datos:** Registrar información detallada del cliente y especificaciones del evento.
- **Administración Financiera:** Capturar abonos manualmente, calcular saldos pendientes y emitir estados de cuenta o recibos digitales.

**Pasos básicos:**

1. Acceda al módulo de *Agenda Digital* o *Calendario* para comprobar disponibilidad de salones.
2. Haga clic en "Nueva Reservación", capture los datos del cliente, seleccione el salón y añada servicios/equipamientos.
3. En la reservación activa, vaya a "Pagos", ingrese el monto abonado y genere el recibo correspondiente.

### 3. Almacenista (Logística y Control de Inventarios)

El Almacenista se enfoca en la preparación física de los eventos y el control del estado del equipamiento y mobiliario.

**Funcionalidades principales:**

- **Monitoreo Logístico:** Consultar eventos próximos y en curso para prever recursos materiales necesarios.
- **Control del Estado del Inventario:** Supervisar existencias y actualizar estado operativo (Disponible, En Uso, Descompuesto, En Reparación).

**Pasos básicos:**

1. Visualice el módulo de "Próximos Eventos" con el listado de recursos asignados a cada salón.
2. Revise las cantidades solicitadas de mobiliario (mesas, sillas) y equipamiento (bocinas, micrófonos).
3. Si un equipo regresa dañado, acceda a *Inventario*, busque el artículo y cambie su estado a "En Reparación" o "Descompuesto".

### 4. Cliente (Consultas y Solicitudes Autónomas)

El cliente interactúa de forma externa con la plataforma web para gestionar sus solicitudes de eventos.

**Funcionalidades principales:**

- **Generación de Solicitudes:** Crear y enviar solicitudes de reservación seleccionando fechas, horarios y salones.
- **Consulta de Catálogos:** Navegar por servicios y equipamientos organizados por categorías.
- **Seguimiento Financiero:** Consultar estado de reservaciones, desglose de servicios e historial de abonos y saldos.

**Pasos básicos:**

1. Inicie sesión y navegue por el catálogo comercial. Use filtros para revisar dimensiones, tarifas y precios.
2. Ingrese al formulario de "Solicitud de Evento", elija fecha, salón e insumos requeridos. Envíe la solicitud.
3. Acceda a su perfil → "Mis Reservaciones" para verificar el estado de sus eventos y descargar estados de cuenta.

## Guía de instalación

### Requisitos previos

- Python 3.13+
- PostgreSQL 16+
- Git
- Cuenta de Google (para Firebase)

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/BookingRoom.git
cd BookingRoom
```

### 2. Crear y activar un entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Asegúrate de tener PostgreSQL instalado y corriendo. Crea las bases de datos:

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE bookingroom_test;
CREATE DATABASE bookingroom_nuevadata;
\q
```

Las credenciales por defecto en `BookingRoom_Django/settings.py` son:

```python
USER: postgres
PASSWORD: postgres
HOST: localhost
PORT: 5432
```

Si tu PostgreSQL usa credenciales distintas, edita esa sección.

> **Alternativa con SQLite:** Si no tienes PostgreSQL, puedes descomentar la configuración de SQLite en `settings.py` (líneas ~133-138) y comentar la de PostgreSQL.

### 5. Configurar Firebase

El sistema usa Firebase Authentication. Debes crear tu propio proyecto de Firebase.

#### 5.1. Crear un proyecto en Firebase

1. Ve a https://console.firebase.google.com/
2. Haz clic en **Crear un proyecto**
3. Sigue los pasos (puedes desactivar Google Analytics)
4. Una vez creado, ve a **Authentication** → **Sign-in method**
5. Habilita el proveedor **Email/Password**

#### 5.2. Obtener credenciales de backend (Admin SDK)

1. En Firebase Console, ve a **Configuración del proyecto** → **Cuentas de servicio**
2. Haz clic en **Generar nueva clave privada**
3. Se descargará un archivo JSON (ej. `proyecto-firebase-adminsdk-xxxxx.json`)
4. Renómbralo a `firebase-creds.json` y colócalo en `BookingRoom_Django/`

```bash
mv ~/Downloads/tu-archivo.json BookingRoom_Django/firebase-creds.json
```

#### 5.3. Configurar Firebase Web (frontend)

1. En Firebase Console, ve a **Configuración del proyecto** → **General**
2. En "Tus apps", haz clic en **Agregar app** → **Web**
3. Copia el objeto `firebaseConfig` y actualiza el archivo `BookingRoomApp/static/BookingRoomApp/js/firebase-auth.js` con los valores de tu proyecto.

### 6. Ejecutar migraciones

```bash
python manage.py makemigrations BookingRoomApp
python manage.py migrate
```

### 7. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 8. Iniciar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en http://127.0.0.1:8000/

### 9. Verificar

- **Web:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/
- **API:** http://127.0.0.1:8000/api/

### Solución de problemas comunes

| Problema | Solución |
|----------|----------|
| `firebase-admin` no se instala | Actualiza pip: `pip install --upgrade pip` |
| El login no funciona | Revisa que `firebase-creds.json` esté en la ruta correcta |
| `role "postgres" does not exist` | `sudo -u postgres createuser --superuser postgres` |
| `FATAL: password authentication failed` | `sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"` |

## Cómo contribuir

Si deseas contribuir al proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Realiza tus cambios y haz commit (`git commit -m 'Agrega nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

> [!IMPORTANT]
> **Código por terminar:** Debido a la metodología de trabajo en la UTT, el proyecto no logró concretarse por completo. Sin embargo, quedó en una etapa muy avanzada.

## Autor/es

- **Gallardo Ramirez Luis David** — luisd.gramirez@gmail.com — Desarrollador front-end
- De La Torre Garcia Ricardo Daniel
- Gonzalez De La Mora Jose Jonathan
- Flores Gomez Kent

## Información adicional

Este proyecto está inspirado en herramientas como **RoomRaccoon**, **Tripleseat** y **Event Temple**.

Además, tiene conexión con una aplicación desarrollada en **Flutter** para dispositivos móviles, sin embargo, la aplicación web puede existir sin la necesidad de ocupar la aplicación movil ya que esta es complementaria.

## Limitaciones del sistema

Este sistema prioriza la gestión de los salones como un inventario perecedero, centrando su valor en la optimización del espacio físico y el mobiliario. Esta decisión responde a una estrategia de Revenue Management diseñada para maximizar el RevPAS (ingreso por metro cuadrado disponible), permitiendo al hotel enfocarse en la alta rotación de eventos cortos (juntas corporativas, ruedas de prensa) que no requieren infraestructura compleja de alimentos y bebidas.

Se ha omitido la gestión de menús rotativos para evitar sobrecarga en la arquitectura de datos y simplificar los procesos administrativos. No obstante, el sistema ofrece flexibilidad para integrar proveedores externos de banquetes en el apartado de servicios, trasladando la responsabilidad logística y sanitaria al prestador del servicio.

**Los pagos** se registran manualmente porque el sistema no está conectado con hardware o APIs de punto de venta. El contrato estándar de arrendamiento estipula pagos en efectivo o cheques certificados, procesos que requieren intervención humana. Se plantea automatizarlo en el futuro.

**Planos 3D** de eventos no están soportados por la complejidad de desarrollo y consumo de recursos. Se prioriza la funcionalidad operativa básica: generación del BEO (Banquet Event Order), control de disponibilidad de salones y gestión de pagos informativa.
