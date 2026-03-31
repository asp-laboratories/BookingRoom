from rest_framework import serializers
from django.contrib.auth.models import User
from BookingRoomApp import models


class TipoEquipaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoEquipa
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoServicio
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rol
        fields = '__all__'


class EstadoCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoCuenta
        fields = '__all__'


class TipoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoCliente
        fields = '__all__'


class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cuenta
        fields = '__all__'


class CuentaMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cuenta
        fields = ['id', 'nombre_usuario', 'correo_electronico']


class TrabajadorSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    rol_codigo = serializers.CharField(source='rol.codigo', read_only=True)
    cuenta_nombre = serializers.CharField(source='cuenta.nombre_usuario', read_only=True)
    
    class Meta:
        model = models.Trabajador
        fields = '__all__'


class DatosClienteSerializer(serializers.ModelSerializer):
    tipo_cliente_nombre = serializers.CharField(source='tipo_cliente.nombre', read_only=True)
    cuenta_nombre = serializers.CharField(source='cuenta.nombre_usuario', read_only=True)
    
    class Meta:
        model = models.DatosCliente
        fields = '__all__'


class LoginResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    email = serializers.EmailField()
    tipo = serializers.CharField()
    rol = serializers.CharField(allow_null=True)


class EncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Encuesta
        fields = '__all__'


class ReservacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservacion
        fields = '__all__'


class RegistrEstadReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegistrEstadReserva
        fields = '__all__'


class ReservaEquipaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReservaEquipa
        fields = '__all__'


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pago
        fields = '__all__'


class ConceptoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConceptoPago
        fields = '__all__'


class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetodoPago
        fields = '__all__'


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Servicio
        fields = '__all__'


class EstadoReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoReserva
        fields = '__all__'


class EquipamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equipamiento
        fields = '__all__'


class InventarioEquipaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InventarioEquipa
        fields = '__all__'


class EstadoEquipaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoEquipa
        fields = '__all__'


class EstadoSalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoSalon
        fields = '__all__'


class RegistrEstadSalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RegistrEstadSalon
        fields = '__all__'


class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Salon
        fields = '__all__'


class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoEvento
        fields = '__all__'


class MontajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Montaje
        fields = '__all__'


class TipoMontajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoMontaje
        fields = '__all__'


class MobiliarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mobiliario
        fields = '__all__'


class MontajeMobiliarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MontajeMobiliario
        fields = '__all__'


class InventarioMobSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InventarioMob
        fields = '__all__'


class EstadoMobilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoMobil
        fields = '__all__'


class CaracterMobilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CaracterMobil
        fields = '__all__'


class TipoMobilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoMobil
        fields = '__all__'


# Aca van todos los personalizados chamos cuidado con estos q estan canijos

class MontajeLecturaSerializer(serializers.ModelSerializer):
    salon = SalonSerializer(read_only=True)
    tipo_montaje = TipoMontajeSerializer(read_only=True)
    montaje_mobiliario = MontajeMobiliarioSerializer(
        source='montajemobiliario_set', 
        many=True, 
        read_only=True
    )

    class Meta:
        model = models.Montaje
        fields = ['id', 'costo', 'salon', 'tipo_montaje', 'montaje_mobiliario']

class MobiliariosMontajeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cantidad = serializers.IntegerField()

class ServiciosReservacionSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class EquipamientoReservacionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cantidad = serializers.IntegerField()

class MontajeCreacionSerializer(serializers.Serializer):
    salon = serializers.IntegerField()
    tipo_montaje = serializers.IntegerField()
    mobiliarios = MobiliariosMontajeSerializer(many=True)

class ReservacionCreacionSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    descripEvento = serializers.CharField()
    estimaAsistentes = serializers.IntegerField()
    fechaEvento = serializers.DateField()
    horaInicio = serializers.TimeField()
    horaFin = serializers.TimeField()
    subtotal = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2)
    IVA = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2)
    total = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2)
    cliente = serializers.IntegerField()
    trabajador = serializers.IntegerField()
    reserva_servicio = ServiciosReservacionSerializer(many=True, required=False, allow_empty=True)
    reserva_equipa = EquipamientoReservacionSerializer(many=True, required=False, allow_empty=True)
    montaje = MontajeCreacionSerializer()
    tipo_evento = serializers.IntegerField()

class ReservacionLecturaSerializer(serializers.ModelSerializer):
    cliente = DatosClienteSerializer(read_only=True)
    montaje = MontajeLecturaSerializer(read_only=True)
    estado_reserva = EstadoReservaSerializer(read_only=True)
    tipo_evento = TipoEventoSerializer(read_only=True)
    trabajador = TrabajadorSerializer(read_only=True)
    reserva_servicio = ServiciosReservacionSerializer(many=True, read_only=True)
    reserva_equipa = ReservaEquipaSerializer(source='reservaequipa_set' ,many=True, read_only=True)

    class Meta:
        model = models.Reservacion
        fields = ['id', 'nombre', 'descripEvento', 
                  'estimaAsistentes', 'fechaReservacion', 
                  'fechaEvento', 'horaInicio', 'horaFin', 
                  'subtotal', 'IVA', 'total', 'cliente', 
                  'montaje', 'estado_reserva', 'tipo_evento', 
                  'trabajador', 'reserva_servicio', 'reserva_equipa']

class ReservacionUpdateSerializer(serializers.Serializer):
    nombre = serializers.CharField(required=False)
    descripEvento = serializers.CharField(required=False)
    estimaAsistentes = serializers.IntegerField(required=False)
    fechaEvento = serializers.DateField(required=False)
    horaInicio = serializers.TimeField(required=False)
    horaFin = serializers.TimeField(required=False)
    subtotal = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    IVA = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    total = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
    cliente = serializers.IntegerField(required=False)
    trabajador = serializers.IntegerField(required=False)
    tipo_evento = serializers.IntegerField(required=False)
    tipo_montaje = serializers.IntegerField(required=False)
    mobiliarios = MobiliariosMontajeSerializer(required=False, many=True)
    reserva_servicio = ServiciosReservacionSerializer(required=False, many=True, allow_empty=True)
    reserva_equipa = EquipamientoReservacionSerializer(many=True, required=False, allow_empty=True)