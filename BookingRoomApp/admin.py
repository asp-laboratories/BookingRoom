from django.contrib import admin
from . import models

@admin.register(models.DatosCliente)
class DatosClienteAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'nombre', 'apellidoPaterno', 'correo_electronico', 'tipo_cliente')
    search_fields = ('rfc', 'nombre', 'correo_electronico')
    list_filter = ('tipo_cliente',)

@admin.register(models.Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('no_empleado', 'nombre', 'rol', 'correo_electronico')
    search_fields = ('no_empleado', 'nombre', 'rfc')
    list_filter = ('rol',)

@admin.register(models.Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado_salon', 'maxCapacidad', 'costo')
    search_fields = ('nombre', 'ubicacion')
    list_filter = ('estado_salon',)

@admin.register(models.Reservacion)
class ReservacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'fechaEvento', 'cliente', 'estado_reserva', 'total')
    search_fields = ('id', 'cliente__nombre', 'cliente__rfc') 
    list_filter = ('estado_reserva', 'fechaEvento', 'tipo_evento')

@admin.register(models.Montaje)
class MontajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'salon', 'tipo_montaje', 'costo')
    list_filter = ('tipo_montaje', 'salon')

@admin.register(models.Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_servicio', 'costo', 'disposicion')
    list_filter = ('tipo_servicio', 'disposicion')

@admin.register(models.Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('no_pago', 'reservacion', 'concepto_pago', 'metodo_pago', 'monto', 'fecha')
    list_filter = ('concepto_pago', 'metodo_pago', 'fecha')
    search_fields = ('no_pago', 'reservacion__id')

@admin.register(models.RegistrEstadReserva)
class RegistrEstadReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'reservacion', 'estado_reserva', 'fecha')
    readonly_fields = ('fecha',) 

@admin.register(models.RegistrEstadSalon)
class RegistrEstadSalonAdmin(admin.ModelAdmin):
    list_display = ('id', 'salon', 'estado_salon', 'fecha')
    readonly_fields = ('fecha',)

catalogos_y_secundarias = [
    models.TipoServicio, models.Rol, models.EstadoCuenta, models.TipoCliente,
    models.Cuenta, models.EstadoMobil, models.CaracterMobil, models.TipoMobil, 
    models.TipoMontaje, models.TipoEvento, models.EstadoReserva, models.EstadoSalon, 
    models.TipoEquipa, models.EstadoEquipa, models.ConceptoPago, models.MetodoPago,
    models.Mobiliario, models.Equipamiento, models.MontajeMobiliario, 
    models.InventarioEquipa, models.InventarioMob, models.ReservaEquipa,
    models.Encuesta, models.ReservaServicio
]

for modelo in catalogos_y_secundarias:
    try:
        admin.site.register(modelo)
    except admin.sites.AlreadyRegistered:
        pass