from django.db import models


# Create your models here.


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
