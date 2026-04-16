from django.db import models
from django.utils import timezone


# Create your models here.
# Modelos de catalogo
class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=550, blank=True)
    disposicion = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'tipo_servicio'
        verbose_name = "Tipo de servicio"
        verbose_name_plural = "Tipos de servicios"
        
    
    def __str__(self):
        return self.nombre


class Rol(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'rol'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.codigo


class EstadoCuenta(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_cuenta'
        verbose_name = "Estado de cuenta"
        verbose_name_plural = "Estados de cuenta"

    def __str__(self):
        return self.codigo


class TipoCliente(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_cliente'
        verbose_name = "Tipo de cliente"
        verbose_name_plural = "Tipos de clientes"

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    firebase_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)
    estado_cuenta = models.ForeignKey(EstadoCuenta, on_delete=models.CASCADE)
    # === IMAGEN DE PERFIL (comentado para revisión) ===
    # Descomentar después de ejecutar migraciones
    # imagen_url = models.URLField(null=True, blank=True, help_text="URL de la imagen de perfil en Firebase Storage")

    class Meta:
        db_table = 'cuenta'
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return self.correo_electronico


class Trabajador(models.Model):
    no_empleado = models.CharField(max_length=10, primary_key=True)
    rfc = models.CharField(max_length=13)
    nombre = models.CharField(max_length=150)
    apellidoPaterno = models.CharField(max_length=150)
    apelidoMaterno = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)

    class Meta:
        db_table = 'trabajador'
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"

    def __str__(self):
        return self.no_empleado


class DatosCliente(models.Model):
    rfc = models.CharField(max_length=13)
    nombre_fiscal = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    apellidoPaterno = models.CharField(max_length=150)
    apelidoMaterno = models.CharField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    dir_colonia = models.CharField(max_length=150)
    dir_calle = models.CharField(max_length=150)
    dir_numero = models.CharField( max_length=50)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, null=True, blank=True, on_delete=models.CASCADE)
    # TODO: Actualizar - Campo para saber si el cliente tiene cuenta en la app
    # registrado_desde_app = models.BooleanField(null=True, blank=True, default=None)

    # === cliente-validar: Lógica para aceptar/rechazar solicitudes ===
    # Cuando el cliente envía solicitud desde la app:
    #   - guardar DatosCliente con registrado_desde_app = None (pendiente)
    #
    # En el admin/web cuando el recepcionista ACEPTA la reservación:
    #   - actualizar DatosCliente: registrado_desde_app = True (confirmado)
    #   - ejemplo: DatosCliente.objects.filter(id=reservacion.cliente_id).update(registrado_desde_app=True)
    #
    # En el admin/web cuando el recepcionista RECHAZA la reservación:
    #   - eliminar DatosCliente del cliente
    #   - ejemplo: DatosCliente.objects.filter(id=reservacion.cliente_id).delete()
    # === cliente-validar: Fin ===

    class Meta:
        db_table = 'datos_cliente'
        verbose_name = "Datos del cliente"
        verbose_name_plural = "Datos de clientes"

    def __str__(self):
        return self.correo_electronico
        
    # def get_absolute_url(self):
    #     return reverse("TipoServicio_detail", kwargs={"pk": self.pk})


class EstadoMobil(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_mobil'
        verbose_name = "Estado de mobiliario"
        verbose_name_plural = "Estados de mobiliario"

    def __str__(self):
        return self.codigo


class CaracterMobil(models.Model):
    descripcion = models.CharField(max_length=550)

    class Meta:
        db_table = 'caracter_mobi'
        verbose_name = "Característica de mobiliario"
        verbose_name_plural = "Caracteristicas de mobiliarios"

    def __str__(self):
        return self.descripcion


class TipoMobil(models.Model):
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_mobil'
        verbose_name = "Tipo de mobiliario"
        verbose_name_plural = "Tipos de mobiliario"

    def __str__(self):
        return self.nombre


class TipoMontaje(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True)
    disposicion = models.BooleanField(default=True)
    capacidadIdeal = models.IntegerField(default=0)

    class Meta:
        db_table = 'tipo_montaje'
        verbose_name = "Tipo de montaje"
        verbose_name_plural = "Tipos de montaje"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.descripcion:
            self.descripcion = f"Montaje en forma {self.nombre}"
        super().save(*args, **kwargs)


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_evento'
        verbose_name = "Tipo de evento"
        verbose_name_plural = "Tipos de evento"

    def __str__(self):
        return self.nombre


class EstadoReserva(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_reserva'
        verbose_name = "Estado de reservacion"
        verbose_name_plural = "Estados de reservacion"

    def __str__(self):
        return self.codigo


class EstadoSalon(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_salon'
        verbose_name = "Estado de salón"
        verbose_name_plural = "Estados de salon"

    def __str__(self):
        return self.codigo


class TipoEquipa(models.Model):
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_equipa'
        verbose_name = "Tipo de equipamiento"
        verbose_name_plural = "Tipos de equipamiento"

    def __str__(self):
        return self.nombre


class EstadoEquipa(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_equipa'
        verbose_name = "Estado de equipamiento"
        verbose_name_plural = "Estados de equipamiento"

    def __str__(self):
        return self.codigo


class ConceptoPago(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'concepto_pago'
        verbose_name = "Concepto de pago"
        verbose_name_plural = "Conceptos de pago"

    def __str__(self):
        return self.codigo


class MetodoPago(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'metodo_pago'
        verbose_name = "Método de pago"
        verbose_name_plural = "Metodos de pago"

    def __str__(self):
        return self.codigo


# Modelos de entidades con relaciones y asi

class Salon(models.Model):
    nombre = models.CharField(max_length=50)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=100)
    dimenLargo = models.DecimalField(max_digits=10, decimal_places=2)
    dimenAncho = models.DecimalField(max_digits=10, decimal_places=2)
    dimenAlto = models.DecimalField(max_digits=10, decimal_places=2)
    metrosCuadrados = models.DecimalField(max_digits=10, decimal_places=2)
    maxCapacidad = models.IntegerField()
    estado_salon = models.ForeignKey(EstadoSalon, on_delete=models.CASCADE)

    class Meta:
        db_table = 'salon'
        verbose_name = 'Salon'
        verbose_name_plural = "Salones"

    def __str__(self):
        return self.nombre


class Montaje(models.Model):
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    tipo_montaje = models.ForeignKey(TipoMontaje, on_delete=models.CASCADE)

    class Meta:
        db_table = 'montaje'
        verbose_name = 'Montaje'
        verbose_name_plural = "Montajes"

    def __str__(self):
        return f"ID:{self.pk} S:{self.salon.nombre} TM:{self.tipo_montaje.nombre}"


class Servicio(models.Model):
    nombre = models.CharField(max_length=75)
    descripcion = models.CharField(max_length=550)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    disposicion = models.BooleanField()
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'servicio'
        verbose_name = 'Servicio'
        verbose_name_plural = "Servicios"

    def __str__(self):
        return str(self.pk)


class Reservacion(models.Model):
    # nombre = models.CharField(max_length=100, blank=True, default="")
    nombreEvento = models.CharField(max_length=100, blank=True, default="")
    descripEvento = models.CharField(max_length=550, blank=True, default="")
    estimaAsistentes = models.IntegerField(null=True, blank=True)
    fechaReservacion = models.DateField(auto_now_add=True)
    fechaEvento = models.DateField(null=True, blank=True)
    horaInicio = models.TimeField(null=True, blank=True)
    horaFin = models.TimeField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    IVA = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cliente = models.ForeignKey(DatosCliente, on_delete=models.CASCADE, null=True, blank=True)
    montaje = models.ForeignKey(Montaje, on_delete=models.CASCADE, null=True, blank=True)
    estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE, null=True, blank=True)
    es_paquete = models.BooleanField(default=False)
    nombre_paquete = models.CharField(max_length=100, blank=True, default="")
    
    # === Sistema de Checklists ===
    checklist_coordinador = models.JSONField(default=dict, blank=True)
    checklist_almacenista = models.JSONField(default=dict, blank=True)
    progreso_checklist = models.FloatField(default=0.0)

    # === cliente-validar: Aceptar/Rechazar reservación ===
    # Al ACEPTAR una reservación desde web/admin:
    #   - actualizar estado_reserva al estado correspondiente
    #   - actualizar DatosCliente: datos_cliente.registrado_desde_app = True
    #   - ejemplo: 
    #       reserva = Reservacion.objects.get(id=reserva_id)
    #       reserva.estado_reserva = EstadoReserva.objects.get(codigo='CONF')
    #       reserva.save()
    #       DatosCliente.objects.filter(id=reserva.cliente_id).update(registrado_desde_app=True)
    #
    # Al RECHAZAR una reservación desde web/admin:
    #   - actualizar estado_reserva al estado de rechazado
    #   - ELIMINAR DatosCliente del cliente (datos no aceptados)
    #   - ejemplo:
    #       reserva = Reservacion.objects.get(id=reserva_id)
    #       cliente_id = reserva.cliente_id
    #       reserva.estado_reserva = EstadoReserva.objects.get(codigo='CANC')
    #       reserva.save()
    #       DatosCliente.objects.filter(id=cliente_id).delete()
    # === cliente-validar: Fin ===

    class Meta:
        db_table = 'reservacion'
        verbose_name = 'Reservacion'
        verbose_name_plural = "Reservaciones"

    def __str__(self):
        return str(self.pk)
    

class Mobiliario(models.Model):
    nombre = models.CharField(max_length=75)
    descripcion = models.CharField(max_length=550)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    tipo_movil = models.ForeignKey(TipoMobil, on_delete=models.CASCADE)
    descripcion_mob = models.ManyToManyField(CaracterMobil)

    class Meta:
        db_table = 'mobiliario'
        verbose_name = 'Mobiliario'
        verbose_name_plural = "Mobiliarios"

    def __str__(self):
        return self.nombre


class MontajeMobiliario(models.Model):
    cantidad = models.IntegerField()
    extra = models.BooleanField(default=False, blank=True, null=True)
    completado = models.BooleanField(default=False, blank=True, null=True)
    montaje = models.ForeignKey(Montaje, on_delete=models.CASCADE)
    mobiliario = models.ForeignKey(Mobiliario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'montaje_mobiliario'
        verbose_name = 'Mobiliarios de un montaje'
        verbose_name_plural = "Mobilarios de montajes"

    def __str__(self):
        return f"Mob:{self.mobiliario.nombre} Mon:{self.montaje.id}"


class Equipamiento(models.Model):
    nombre = models.CharField(max_length=75)
    descripcion = models.CharField(max_length=550)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    tipo_equipa = models.ForeignKey(TipoEquipa, on_delete=models.CASCADE)

    class Meta:
        db_table = 'equipamiento'
        verbose_name = 'Equipamiento'
        verbose_name_plural = "Equipamientos"
    
    def __str__(self):
        return str(self.pk)


class InventarioEquipa(models.Model):
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    estado_equipa = models.ForeignKey(EstadoEquipa, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'inventario_equipa'
        verbose_name = 'Inventario de equipamiento'
        verbose_name_plural = "Inventarios de equipamiento"

        constraints = [
            models.UniqueConstraint(
                fields= ['equipamiento', 'estado_equipa'],
                name= 'estado_equipamiento'
            )
        ]

    def __str__(self):
        return f"Eq:{self.equipamiento.pk} Es:{self.estado_equipa.pk}"


class InventarioMob(models.Model):
    mobiliario = models.ForeignKey(Mobiliario, on_delete=models.CASCADE)
    estado_mobil = models.ForeignKey(EstadoMobil, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'inventario_mobil'
        verbose_name = "Inventario de mobilario"
        verbose_name_plural = "Inventarios de mobiliario"

        constraints = [
            models.UniqueConstraint(
                fields= ['mobiliario', 'estado_mobil'],
                name= 'estado_mobiliario'
            )
        ]

    def __str__(self):
        return f"M:{self.mobiliario.pk} E:{self.estado_mobil.pk}"


class ReservaServicio(models.Model):
    extra = models.BooleanField(default=False, blank=True, null=True)
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reserva_servicio'
        verbose_name = 'Servicios de reservacion'
        verbose_name_plural = 'Servicios de reservaciones'
    
    def __str__(self):
        return f"R:{self.reservacion.pk} S:{self.servicio.pk}"


class ReservaEquipa(models.Model):
    cantidad = models.IntegerField()
    extra = models.BooleanField(default=False, blank=True, null=True)
    completado = models.BooleanField(default=False, blank=True, null=True)
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reserva_equipa'
        verbose_name = 'Equipamientos de reservacion'
        verbose_name_plural = "Equipamientos de reservaciones"

    def __str__(self):
        return f"R:{self.reservacion.pk} E:{self.equipamiento.pk} C:{self.cantidad}"


class RegistrEstadReserva(models.Model):
    fecha = models.DateField(auto_now=True, null=True, blank=True)
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)
    estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.CASCADE)

    class Meta:
        db_table = 'registr_esta_reserva'
        verbose_name = 'Registro de estado de reservacion'
        verbose_name_plural = "Registros de estados de reservaciones"

    def __str__(self):
        return f"R:{self.reservacion.pk} E:{self.estado_reserva.pk}"


class RegistrEstadSalon(models.Model):
    fecha = models.DateField(null=True, blank=True, default=timezone.now)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    estado_salon = models.ForeignKey(EstadoSalon, on_delete=models.CASCADE)
    # Campo para especificar la fecha fin del estado (para estados limitados en el tiempo)
    # fecha_fin = models.DateField(null=True, blank=True, help_text="Fecha fin del estado (opcional)")

    class Meta:
        db_table = 'registr_esta_salon'
        verbose_name = 'Registro de estado de salon'
        verbose_name_plural = "Registros de estados de salones"
    
    def __str__(self):
        return f"S:{self.salon.pk} E:{self.estado_salon.pk}"


class Encuesta(models.Model):
    personal = models.IntegerField()
    equipamiento = models.IntegerField()
    servicios = models.IntegerField()
    salon = models.IntegerField()
    mobiliario = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)

    class Meta:
        db_table = 'encuesta'
        verbose_name = 'Encuesta'
        verbose_name_plural = "Encuestas"

    def __str__(self):
        return str(self.pk)
    

class Pago(models.Model):
    nota = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha = models.DateField(auto_now=True)
    hora = models.TimeField(auto_now=True)
    no_pago = models.IntegerField()
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)
    concepto_pago = models.ForeignKey(ConceptoPago, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pago'
        verbose_name = 'Pago'
        verbose_name_plural = "Pagos"

    def __str__(self):
        return f"P:{self.no_pago} R:{self.reservacion.pk}"