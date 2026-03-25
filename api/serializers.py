from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Sum
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

class FechasReservaciones(serializers.ModelSerializer):
    class Meta:
        model = models.Reservacion
        fields = ['nombreEvento','fechaEvento',]

class PagoSerializer(serializers.ModelSerializer):
    no_pago = serializers.IntegerField(read_only=True)
    saldo = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    concepto_pago = serializers.CharField(write_only=True, required=False)
    metodo_pago = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = models.Pago
        fields = ['nota', 'monto', 'saldo', 'no_pago', 'reservacion', 'concepto_pago', 'metodo_pago', 'fecha', 'hora']
        read_only_fields = ['fecha', 'hora', 'no_pago', 'saldo']
    
    def create(self, validated_data):
        concepto_codigo = validated_data.pop('concepto_pago', None)
        metodo_codigo = validated_data.pop('metodo_pago', None)
        
        if concepto_codigo:
            validated_data['concepto_pago'] = models.ConceptoPago.objects.get(codigo=concepto_codigo)
        if metodo_codigo:
            validated_data['metodo_pago'] = models.MetodoPago.objects.get(codigo=metodo_codigo)
        
        ultimo = models.Pago.objects.order_by('-no_pago').first()
        validated_data['no_pago'] = (ultimo.no_pago + 1) if ultimo else 1
        
        reserva = validated_data['reservacion']
        monto = validated_data['monto']
        pagos_previos = models.Pago.objects.filter(reservacion=reserva).count()
        
        if pagos_previos >= 2:
            raise serializers.ValidationError({'error': 'Esta reservación ya tiene los 2 pagos permitidos'})
        
        if pagos_previos == 0:
            validated_data['saldo'] = reserva.total - monto
        else:
            validated_data['saldo'] = 0
        
        return super().create(validated_data)


class ConceptoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConceptoPago
        fields = '__all__'


class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MetodoPago
        fields = '__all__'


class SerivicioSerializer(serializers.ModelSerializer):
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