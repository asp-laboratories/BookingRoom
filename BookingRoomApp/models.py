from django.db import models


# Create your models here.
# Modelos de catalogo
class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    disposicion = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'tipo_servicio'
        verbose_name = "Tipo de servicio"
    
    def __str__(self):
        return self.nombre


class Rol(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'rol'
        verbose_name = "Rol"

    def __str__(self):
        return self.codigo


class EstadoCuenta(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_cuenta'
        verbose_name = "Estado de cuenta"

    def __str__(self):
        return self.codigo


class TipoCliente(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_cliente'
        verbose_name = "Tipo de cliente"

    def __str__(self):
        return self.nombre


class Cuenta(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    correo_electronico = models.EmailField(unique=True)
    disposicion = models.BooleanField(default=True)
    firebase_uid = models.CharField(max_length=255, unique=True, null=True, blank=True)
    estado_cuenta = models.ForeignKey(EstadoCuenta, on_delete=models.PROTECT)

    class Meta:
        db_table = 'cuenta'
        verbose_name = "Cuenta"

    def __str__(self):
        return self.correo_electronico


class Trabajador(models.Model):
    no_empleado = models.CharField(max_length=10, primary_key=True)
    rfc = models.CharField(max_length=13)
    nombre_fiscal = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    apellidoPaterno = models.CharField(max_length=150)
    apelidoMaterno = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT)

    class Meta:
        db_table = 'trabajador'
        verbose_name = "Trabajador"

    def __str__(self):
        return self.no_empleado


class DatosCliente(models.Model):
    rfc = models.CharField(max_length=13)
    nombre_fiscal = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    apellidoPaterno = models.CharField(max_length=150)
    apelidoMaterno = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(unique=True)
    dir_colonia = models.CharField(max_length=150)
    dir_calle = models.CharField(max_length=150)
    dir_numero = models.CharField( max_length=50)
    tipo_cliente = models.ForeignKey(TipoCliente, on_delete=models.PROTECT)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.PROTECT)

    class Meta:
        db_table = 'datos_cliente'
        verbose_name = "Datos del cliente"

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

    def __str__(self):
        return self.codigo


class CaracterMobil(models.Model):
    descripcion = models.TextField()

    class Meta:
        db_table = 'caracter_mobi'
        verbose_name = "Característica de mobiliario"

    def __str__(self):
        return self.descripcion


class TipoMobil(models.Model):
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_mobil'
        verbose_name = "Tipo de mobiliario"

    def __str__(self):
        return self.nombre


class TipoMontaje(models.Model):
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_montaje'
        verbose_name = "Tipo de montaje"

    def __str__(self):
        return self.nombre


class TipoEvento(models.Model):
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_evento'
        verbose_name = "Tipo de evento"

    def __str__(self):
        return self.nombre


class EstadoReserva(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_reserva'
        verbose_name = "Estado de reserva"

    def __str__(self):
        return self.codigo


class EstadoSalon(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_salon'
        verbose_name = "Estado de salón"

    def __str__(self):
        return self.codigo


class TipoEquipa(models.Model):
    nombre = models.CharField(max_length=100)
    disposicion = models.BooleanField(default=True)

    class Meta:
        db_table = 'tipo_equipa'
        verbose_name = "Tipo de equipamiento"

    def __str__(self):
        return self.nombre


class EstadoEquipa(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'estado_equipa'
        verbose_name = "Estado de equipamiento"

    def __str__(self):
        return self.codigo


class ConceptoPago(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'concepto_pago'
        verbose_name = "Concepto de pago"

    def __str__(self):
        return self.codigo


class MetodoPago(models.Model):
    codigo = models.CharField(max_length=5, primary_key=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        db_table = 'metodo_pago'
        verbose_name = "Método de pago"

    def __str__(self):
        return self.codigo


# Modelos de entidades con relaciones y asi

class Salon(models.Model):
    nombre = models.CharField(max_length=50)
<<<<<<< HEAD
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    ubicacion = models.CharField(max_length=100)
    dimenLargo = models.DecimalField(max_digits=10, decimal_places=2)
    dimenAncho = models.DecimalField(max_digits=10, decimal_places=2)
    dimenAlto = models.DecimalField(max_digits=10, decimal_places=2)
    metrosCuadrados = models.DecimalField(max_digits=10, decimal_places=2)
=======
    costo = models.DecimalField()
    ubicacion = models.CharField(max_length=100)
    dimenLargo = models.DecimalField()
    dimenAncho = models.DecimalField()
    dimenAlto = models.DecimalField()
    metrosCuadrados = models.DecimalField()
>>>>>>> faf36057139c4a4da0cec470ecafa534fb1031c8
    maxCapacidad = models.IntegerField()
    estado_salon = models.ForeignKey(EstadoSalon, on_delete=models.CASCADE)

    class Meta:
        db_table = 'salon'
        verbose_name = 'Salon'

    def __str__(self):
        return self.nombre


class Montaje(models.Model):
<<<<<<< HEAD
    costo = models.DecimalField(max_digits=10, decimal_places=2)
=======
    costo = models.DecimalField()
>>>>>>> faf36057139c4a4da0cec470ecafa534fb1031c8
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    tipo_montaje = models.ForeignKey(TipoMontaje, on_delete=models.CASCADE)

    class Meta:
        db_table = 'montaje'
        verbose_name = 'Montaje'

    def __str__(self):
        return f"S:{self.salon.pk} TM:{self.tipo_montaje.pk}"


class Servicio(models.Model):
    nombre = models.CharField(max_length=75)
    descripcion = models.CharField(max_length=150)
<<<<<<< HEAD
    costo = models.DecimalField(max_digits=10, decimal_places=2)
=======
    costo = models.DecimalField()
>>>>>>> faf36057139c4a4da0cec470ecafa534fb1031c8
    disposicion = models.BooleanField()
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'servicio'
        verbose_name = 'Servicio'

    def __str__(self):
        return str(self.pk)


class Reservacion(models.Model):
<<<<<<< HEAD
    descripEvento = models.CharField(max_length=50)
=======
    descripEvento = models.models.CharField(max_length=50)
>>>>>>> faf36057139c4a4da0cec470ecafa534fb1031c8
    estimaAsistentes = models.IntegerField()
    fechaReservacion = models.DateField(auto_now_add=True)
    fechaEvento = models.DateField()
    horaInicio = models.TimeField()
    horaFin = models.TimeField()
<<<<<<< HEAD
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    IVA = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
=======
    subtotal = models.DecimalField()
    IVA = models.DecimalField()
    total = models.DecimalField()
>>>>>>> faf36057139c4a4da0cec470ecafa534fb1031c8
    cliente = models.ForeignKey(DatosCliente, on_delete=models.CASCADE)
    montaje = models.ForeignKey(Montaje, on_delete=models.CASCADE)
    estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.CASCADE)
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE)
    reserva_servicio = models.ManyToManyField(Servicio)
    traba_reserva = models.ManyToManyField(Trabajador)

    class Meta:
        db_table = 'reservacion'
        verbose_name = 'Reservacion'

    def __str__(self):
        return str(self.pk)
    

class Mobiliario(models.Model):
    nombre = models.CharField(max_length=75)
    descripcion = models.CharField(max_length=150)
<<<<<<< HEAD
    costo = models.DecimalField(max_digits=10, decimal_places=2)
=======
    costo = models.DecimalField()
>>>>>>> faf36057139c4a4da0cec470ecafa534fb1031c8
    stock = models.IntegerField()
    tipo_movil = models.ForeignKey(TipoMobil, on_delete=models.CASCADE)
    descripcion_mob = models.ManyToManyField(CaracterMobil)

    class Meta:
        db_table = 'mobiliario'
        verbose_name = 'Mobiliario'

    def __str__(self):
        return self.nombre


class MontajeMobiliario(models.Model):
    cantidad = models.IntegerField()
    completado = models.BooleanField(default=False)
    montaje = models.ForeignKey(Montaje, on_delete=models.CASCADE)
    mobiliario = models.ForeignKey(Mobiliario, on_delete=models.CASCADE)

    class Meta:
        db_table = 'montaje_mobilairio'
        verbose_name = 'Mobiliarios de un Montaje'

    def __str__(self):
        return f"Mob:{self.montaje.pk} Mon:{self.mobiliario.pk}"


class Equipamiento(models.Model):
    nombre = models.CharField(max_length=75)
    descripcion = models.CharField(max_length=150)
<<<<<<< HEAD
    costo = models.DecimalField(max_digits=10, decimal_places=2)
=======
    costo = models.DecimalField()
>>>>>>> faf36057139c4a4da0cec470ecafa534fb1031c8
    stock = models.IntegerField()
    tipo_equipa = models.ForeignKey(TipoEquipa, on_delete=models.CASCADE)

    class Meta:
        db_table = 'equipamiento'
        verbose_name = 'Equipamiento'
    
    def __str__(self):
        return str(self.pk)


class InventarioEquipa(models.Model):
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)
    estado_equipa = models.ForeignKey(EstadoEquipa, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'inventario_equipa'
        verbose_name = 'Estado de Equipamientos'

        constraints = [
            models.UniqueConstraint(
                fields= ['equipamiento', 'esado_equipa'],
                name= 'estado_equipamiento'
            )
        ]

    def __str__(self):
        return f"E:{self.equipamiento.pk} E:{self.estado_equipa.pk}"


class InventarioMob(models.Model):
    mobiliario = models.ForeignKey(Mobiliario, on_delete=models.CASCADE)
    estado_mobil = models.ForeignKey(EstadoMobil, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    class Meta:
        db_table = 'inventario_mobil'
        verbose_name = "Estado de Mobilarios"

        constraints = [
            models.UniqueConstraint(
                fields= ['mobiliario', 'estado_mobil'],
                name= 'estado_mobiliario'
            )
        ]

    def __str__(self):
        return f"M:{self.mobiliario.pk} E:{self.estado_mobil.pk}"


class ReservaEquipa(models.Model):
    cantidad = models.IntegerField()
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)
    equipamiento = models.ForeignKey(Equipamiento, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reserva_equipa'
        verbose_name = 'Equipamientos de Reserva'

    def __str__(self):
        return f"R:{self.reservacion.pk} E:{self.equipamiento.pk} C:{self.cantidad}"


class RegistrEstadReserva(models.Model):
    fecha = models.DateField(auto_now=True)
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)
    estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.CASCADE)

    class Meta:
        db_table = 'registr_esta_reserva'
        verbose_name = 'Registro de estados de Reservacion'

    def __str__(self):
        return f"R:{self.reservacion.pk} E:{self.estado_reserva.pk}"


class RegistrEstadSalon(models.Model):
    fecha = models.DateField(auto_now=True)
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    estado_salon = models.ForeignKey(EstadoSalon, on_delete=models.CASCADE)

    class Meta:
        db_table = 'registr_esta_salon'
        verbose_name = 'Registro de estados de Salon'
    
    def __str__(self):
        return f"S:{self.salon.pk} E:{self.estado_salon.pk}"


class Encuesta(models.Model):
    personal = models.IntegerField()
    equipamiento = models.IntegerField()
    servicios = models.IntegerField()
    salon = models.IntegerField()
    mobiliario = models.IntegerField()
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)

    class Meta:
        db_table = 'encuesta'
        verbose_name = 'Encuesta'

    def __str__(self):
        return str(self.pk)
    

class Pago(models.Model):
    nota = models.CharField(max_length=100)
<<<<<<< HEAD
    monto = models.DecimalField(max_digits=10, decimal_places=2)
=======
    monto = models.DecimalField()
>>>>>>> faf36057139c4a4da0cec470ecafa534fb1031c8
    fecha = models.DateField(auto_now=True)
    hora = models.TimeField(auto_now=True)
    no_pago = models.IntegerField()
    reservacion = models.ForeignKey(Reservacion, on_delete=models.CASCADE)
    concepto_pago = models.ForeignKey(ConceptoPago, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)

    class Meta:
        db_table = 'pago'
        verbose_name = 'Pago'

    def __str__(self):
        return f"P:{self.no_pago} R:{self.reservacion.pk}"