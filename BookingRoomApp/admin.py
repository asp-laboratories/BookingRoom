from django.contrib import admin
from .models import TipoServicio, Trabajador, Rol, DatosCliente, Cuenta, EstadoCuenta, TipoCliente

admin.site.register(TipoServicio)
admin.site.register(Trabajador)
admin.site.register(Rol)
admin.site.register(DatosCliente)
admin.site.register(Cuenta)
admin.site.register(EstadoCuenta)
admin.site.register(TipoCliente)
