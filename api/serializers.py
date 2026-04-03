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


class ReservacionCreacionSerializer(serializers.ModelSerializer):
    trabajador_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = models.Reservacion
        fields = '__all__'
        extra_kwargs = {'trabajador': {'required': False}}

    def create(self, validated_data):
        trabajador_id = validated_data.pop('trabajador_id', None)
        if trabajador_id:
            try:
                trabajador = models.Trabajador.objects.get(no_empleado=str(trabajador_id))
                validated_data['trabajador'] = trabajador
            except models.Trabajador.DoesNotExist:
                pass
        return super().create(validated_data)


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
    
    # Campos adicionales para el comprobante
    subtotal = serializers.SerializerMethodField()
    iva = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    fecha_evento = serializers.SerializerMethodField()
    hora_inicio = serializers.SerializerMethodField()
    hora_fin = serializers.SerializerMethodField()
    salon = serializers.SerializerMethodField()
    montaje = serializers.SerializerMethodField()
    servicios = serializers.SerializerMethodField()
    lista_equipamentos = serializers.SerializerMethodField()
    atendido_por = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Pago
        fields = ['nota', 'monto', 'saldo', 'no_pago', 'reservacion', 'concepto_pago', 'metodo_pago', 'fecha', 'hora',
                  'subtotal', 'iva', 'total', 'fecha_evento', 'hora_inicio', 'hora_fin', 
                  'salon', 'montaje', 'servicios', 'lista_equipamentos', 'atendido_por']
        read_only_fields = ['fecha', 'hora', 'no_pago', 'saldo', 'subtotal', 'iva', 'total', 
                            'fecha_evento', 'hora_inicio', 'hora_fin', 'salon', 'montaje', 
                            'servicios', 'lista_equipamentos', 'atendido_por']
    
    def get_subtotal(self, obj):
        try:
            return str(obj.reservacion.subtotal) if obj.reservacion else '0.00'
        except:
            return '0.00'
    
    def get_iva(self, obj):
        try:
            return str(obj.reservacion.IVA) if obj.reservacion else '0.00'
        except:
            return '0.00'
    
    def get_total(self, obj):
        try:
            return str(obj.reservacion.total) if obj.reservacion else '0.00'
        except:
            return '0.00'
    
    def get_fecha_evento(self, obj):
        try:
            return obj.reservacion.fechaEvento.strftime('%Y-%m-%d') if obj.reservacion and obj.reservacion.fechaEvento else '—'
        except:
            return '—'
    
    def get_hora_inicio(self, obj):
        try:
            return obj.reservacion.horaInicio.strftime('%H:%M') if obj.reservacion and obj.reservacion.horaInicio else '—'
        except:
            return '—'
    
    def get_hora_fin(self, obj):
        try:
            return obj.reservacion.horaFin.strftime('%H:%M') if obj.reservacion and obj.reservacion.horaFin else '—'
        except:
            return '—'
    
    def get_salon(self, obj):
        try:
            if obj.reservacion and obj.reservacion.montaje and obj.reservacion.montaje.salon:
                return obj.reservacion.montaje.salon.nombre
        except:
            pass
        return '—'
    
    def get_montaje(self, obj):
        try:
            if obj.reservacion and obj.reservacion.montaje and obj.reservacion.montaje.tipo_montaje:
                return obj.reservacion.montaje.tipo_montaje.nombre
        except:
            pass
        return '—'
    
    def get_servicios(self, obj):
        try:
            if obj.reservacion:
                return list(obj.reservacion.reserva_servicio.values_list('nombre', flat=True))
        except:
            pass
        return []
    
    def get_lista_equipamentos(self, obj):
        try:
            if obj.reservacion:
                return list(obj.reservacion.reserva_equipa.select_related('equipamiento').values_list('equipamiento__nombre', flat=True))
        except:
            pass
        return []
    
    def get_atendido_por(self, obj):
        return 'Recepción'
    
    def create(self, validated_data):
        concepto_codigo = validated_data.pop('concepto_pago', None)
        metodo_codigo = validated_data.pop('metodo_pago', None)
        
        try:
            if concepto_codigo:
                validated_data['concepto_pago'] = models.ConceptoPago.objects.get(codigo=concepto_codigo)
        except models.ConceptoPago.DoesNotExist:
            raise serializers.ValidationError({'concepto_pago': f'Concepto de pago {concepto_codigo} no encontrado'})
        
        try:
            if metodo_codigo:
                validated_data['metodo_pago'] = models.MetodoPago.objects.get(codigo=metodo_codigo)
        except models.MetodoPago.DoesNotExist:
            raise serializers.ValidationError({'metodo_pago': f'Método de pago {metodo_codigo} no encontrado'})
        
        reserva = validated_data['reservacion']
        monto = validated_data['monto']
        
        # Obtener el último pago de esta reservación específica
        ultimo_pago_reserva = models.Pago.objects.filter(reservacion=reserva).order_by('-no_pago').first()
        
        # Calcular saldo actual (total - suma de pagos anteriores)
        if ultimo_pago_reserva:
            saldo_actual = ultimo_pago_reserva.saldo
        else:
            saldo_actual = reserva.total
        
        # Validar que monto no exceda el saldo pendiente
        if monto > saldo_actual:
            raise serializers.ValidationError({'monto': f'El monto excede el saldo pendiente de ${saldo_actual}'})
        
        if ultimo_pago_reserva:
            validated_data['no_pago'] = ultimo_pago_reserva.no_pago + 1
            validated_data['saldo'] = ultimo_pago_reserva.saldo - monto
        else:
            validated_data['no_pago'] = 1
            validated_data['saldo'] = reserva.total - monto
        
        return super().create(validated_data)


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
    
class ReservaServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReservaServicio
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
    nombre = serializers.CharField() #
    descripEvento = serializers.CharField() #
    estimaAsistentes = serializers.IntegerField() #
    fechaEvento = serializers.DateField() #
    horaInicio = serializers.TimeField() #
    horaFin = serializers.TimeField() #
    subtotal = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2, required=False) # no se obtienen xd
    IVA = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2, required=False) # no se obtienen xd
    total = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2, required=False) # no se obtienen xd
    cliente = serializers.CharField() #
    trabajador = serializers.CharField() #
    estado_reserva = EstadoReservaSerializer(required=False) # automatico como pendiente
    reserva_servicio = ServiciosReservacionSerializer(many=True, required=False, allow_empty=True) #
    reserva_equipa = EquipamientoReservacionSerializer(many=True, required=False, allow_empty=True) #
    montaje = MontajeCreacionSerializer() #
    tipo_evento = serializers.IntegerField()

class ReservacionLecturaSerializer(serializers.ModelSerializer):
    cliente = DatosClienteSerializer(read_only=True)
    montaje = MontajeLecturaSerializer(read_only=True)
    estado_reserva = EstadoReservaSerializer(read_only=True)
    tipo_evento = TipoEventoSerializer(read_only=True)
    trabajador = TrabajadorSerializer(read_only=True)
    reserva_servicio = ReservaServicioSerializer(source='reservaservicio_set' ,many=True, read_only=True)
    reserva_equipa = ReservaEquipaSerializer(source='reservaequipa_set' ,many=True, read_only=True)

    class Meta:
        model = models.Reservacion
        fields = ['id', 'nombreEvento', 'descripEvento', 
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
    estado_reserva = serializers.CharField(required=False)
    reserva_servicio = ServiciosReservacionSerializer(required=False, many=True, allow_empty=True)
    reserva_equipa = EquipamientoReservacionSerializer(many=True, required=False, allow_empty=True)
    
    def to_representation(self, instance):
        return ReservacionLecturaSerializer(instance).data


class ReservacionResumenSerializer(serializers.ModelSerializer):
    """Serializer minimalista para el calendario y vista resumida"""
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    salon = serializers.CharField(source='montaje.salon.nombre', read_only=True)
    
    class Meta:
        model = models.Reservacion
        fields = ['id', 'nombreEvento', 'fechaEvento', 'horaInicio', 'horaFin', 
                  'cliente_nombre', 'salon', 'estado_reserva']