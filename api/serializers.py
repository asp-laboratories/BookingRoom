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
    # === IMAGEN DE PERFIL (comentado para revisión) ===
    # Descomentar después de agregar campo en modelo
    # imagen_url = serializers.URLField(source='imagen_url', read_only=True)
    
    class Meta:
        model = models.Cuenta
        fields = '__all__'
        # === Para incluir imagen_url en la respuesta ===
        # fields = ['id', 'nombre_usuario', 'correo_electronico', 'imagen_url', 'estado_cuenta']


class PerfilSerializer(serializers.Serializer):
    """Serializer para datos del perfil del trabajador"""
    cuenta_id = serializers.IntegerField(source='cuenta.id')
    nombre_usuario = serializers.CharField(source='cuenta.nombre_usuario')
    correo_electronico = serializers.CharField(source='cuenta.correo_electronico')
    no_empleado = serializers.CharField()
    nombre = serializers.CharField()
    apellidoPaterno = serializers.CharField()
    apellidoMaterno = serializers.CharField(allow_null=True)
    telefono = serializers.CharField()
    rfc = serializers.CharField()
    rol_nombre = serializers.CharField(source='rol.nombre')


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


class ReservacionBasicSerializer(serializers.ModelSerializer):
    """Serializer básico para operaciones simples de reservación."""
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
    no_empleado = serializers.SerializerMethodField()
    cliente_nombre = serializers.SerializerMethodField()
    mobiliarios = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Pago
        fields = ['nota', 'monto', 'saldo', 'no_pago', 'reservacion', 'concepto_pago', 'metodo_pago', 'fecha', 'hora',
                  'subtotal', 'iva', 'total', 'fecha_evento', 'hora_inicio', 'hora_fin', 
                  'salon', 'montaje', 'servicios', 'lista_equipamentos', 'atendido_por',
                  'no_empleado', 'cliente_nombre', 'mobiliarios']
        read_only_fields = ['fecha', 'hora', 'no_pago', 'saldo', 'subtotal', 'iva', 'total', 
                            'fecha_evento', 'hora_inicio', 'hora_fin', 'salon', 'montaje', 
                            'servicios', 'lista_equipamentos', 'atendido_por', 'no_empleado', 'cliente_nombre', 'mobiliarios']
    
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
                return list(obj.reservacion.reservaservicio_set.values_list('servicio__nombre', flat=True))
        except Exception as e:
            print('Error get_servicios:', e)
        return []
    
    def get_lista_equipamentos(self, obj):
        try:
            if obj.reservacion:
                return list(obj.reservacion.reservaequipa_set.values_list('equipamiento__nombre', flat=True))
        except Exception as e:
            print('Error get_lista_equipamentos:', e)
        return []
    
    def get_atendido_por(self, obj):
        try:
            if obj.reservacion and obj.reservacion.trabajador and obj.reservacion.trabajador.nombre:
                return obj.reservacion.trabajador.nombre
        except:
            pass
        return 'Recepción'
    
    def get_no_empleado(self, obj):
        try:
            if obj.reservacion and obj.reservacion.trabajador:
                return obj.reservacion.trabajador.no_empleado
        except:
            pass
        return '—'
    
    def get_cliente_nombre(self, obj):
        try:
            if obj.reservacion and obj.reservacion.cliente:
                cliente = obj.reservacion.cliente
                nombre = cliente.nombre or ''
                ap = cliente.apellido_paterno or ''
                am = cliente.apellido_materno or ''
                return f"{nombre} {ap} {am}".strip()
        except Exception as e:
            print('Error get_cliente_nombre:', e)
            pass
        return '—'
    
    def get_mobiliarios(self, obj):
        try:
            if obj.reservacion and obj.reservacion.montaje:
                mobs = obj.reservacion.montaje.montajemobiliario_set.all()
                return [{'tipo': m.mobiliario.nombre, 'cantidad': m.cantidad} for m in mobs]
        except Exception as e:
            print('Error get_mobiliarios:', e)
        return []
    
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
    tipo_servicio = serializers.StringRelatedField()
    costo = serializers.IntegerField()
    
    class Meta:
        model = models.Servicio
        fields = ['id', 'nombre', 'descripcion', 'costo', 'tipo_servicio']


class EstadoReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoReserva
        fields = '__all__'


class EquipamientoSerializer(serializers.ModelSerializer):
    tipo_equipa = serializers.StringRelatedField()
    costo = serializers.IntegerField()
    stock = serializers.IntegerField()
    stockDisponible = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Equipamiento
        fields = ['id', 'nombre', 'descripcion', 'costo', 'stock', 'tipo_equipa', 'stockDisponible']


    def get_stockDisponible(self, obj):
        inventario = models.InventarioEquipa.objects.filter(equipamiento=obj, estado_equipa__codigo__in=['DIS', 'DISP', 'DISPO']).first()
        if inventario:
            return int(inventario.cantidad)
        return 0
        

# class InventarioEquipaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.InventarioEquipa
#         fields = '__all__'
#         depth = 1

class InventarioEquipaSerializer(serializers.ModelSerializer):
    # Esta función se activa automáticamente en los GET (Lectura)
    def to_representation(self, instance):
        # Inyectamos los serializers base para que Flutter reciba 
        # el objeto completo (nombre, imagen, descripción, etc.)
        self.fields['equipamiento'] = EquipamientoSerializer(read_only=True)
        self.fields['estado_equipa'] = EstadoEquipaSerializer(read_only=True)
        return super(InventarioEquipaSerializer, self).to_representation(instance)
    class Meta:
        model = models.InventarioEquipa
        fields = '__all__'
           # NO uses depth=1 aquí, to_representation es más flexible



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
        fields = ['id', 'fecha', 'salon', 'estado_salon']


class SalonEstadoSerializer(serializers.ModelSerializer):
    estado_nombre = serializers.CharField(source='estado_salon.nombre', read_only=True)
    estado_codigo = serializers.CharField(source='estado_salon.codigo', read_only=True)
    
    class Meta:
        model = models.Salon
        fields = ['id', 'nombre', 'estado_salon', 'estado_nombre', 'estado_codigo']


class SalonSerializer(serializers.ModelSerializer):
    precio = serializers.SerializerMethodField()
    capacidad = serializers.SerializerMethodField()
    estado = serializers.SerializerMethodField()
    dimensiones = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Salon
        fields = ['id', 'nombre', 'precio', 'capacidad', 'estado', 'ubicacion', 'dimenLargo', 'dimenAncho', 'dimenAlto', 'metrosCuadrados', 'dimensiones']
    
    def get_precio(self, obj):
        if obj.costo:
            return int(obj.costo)
        return 0
    
    def get_capacidad(self, obj):
        if obj.maxCapacidad:
            return int(obj.maxCapacidad)
        return 0
    
    def get_estado(self, obj):
        if obj.estado_salon:
            return obj.estado_salon.nombre
        return 'Disponible'

    def get_dimensiones(self, obj):
        if obj.dimenLargo and obj.dimenAncho and obj.dimenAlto:
            return f"{obj.dimenAncho}m x {obj.dimenLargo}m x {obj.dimenAlto}m"
        return f"{obj.dimenAncho}m x {obj.dimenAlto}m"


class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoEvento
        fields = '__all__'


class MontajeSerializer(serializers.ModelSerializer):
    salon_nombre = serializers.CharField(source='salon.nombre', read_only=True)
    tipo_montaje_nombre = serializers.CharField(source='tipo_montaje.nombre', read_only=True)
    tipo_montaje_id = serializers.IntegerField(source='tipo_montaje.id', read_only=True)
    
    class Meta:
        model = models.Montaje
        fields = ['id', 'salon', 'salon_nombre', 'tipo_montaje', 'tipo_montaje_nombre', 'tipo_montaje_id', 'costo']


class TipoMontajeSerializer(serializers.ModelSerializer):
    montaje_mobiliario = serializers.SerializerMethodField()

    class Meta:
        model = models.TipoMontaje
        fields = ['id', 'nombre', 'descripcion', 'disposicion', 'capacidadIdeal', 'montaje_mobiliario']

    def get_montaje_mobiliario(self, obj):
        request = self.context.get('request')
        if not request:
            return []
        salon_id = request.query_params.get('salon')
        if not salon_id:
            return []    
        montaje = models.Montaje.objects.filter(tipo_montaje=obj, salon_id=salon_id, montajemobiliario__isnull=False).distinct().order_by('-id').first()
        if not montaje:
            return []
        sugeridos = []
        for item in models.MontajeMobiliario.objects.filter(montaje=montaje):
            sugeridos.append({
                'id': item.mobiliario.id,
                'nombre': item.mobiliario.nombre,
                'cantidad': item.cantidad,
                'costo': item.mobiliario.costo if item.mobiliario.costo else 0
            })
        return sugeridos


class MobiliarioSerializer(serializers.ModelSerializer):
    precio = serializers.SerializerMethodField()
    stockDisponible = serializers.SerializerMethodField()
    caracteristicas = serializers.SerializerMethodField()
    tipo_nombre = serializers.CharField(source='tipo_movil.nombre', read_only=True)
    
    class Meta:
        model = models.Mobiliario
        fields = ['id', 'nombre', 'descripcion', 'precio', 'stock', 'tipo_movil', 'tipo_nombre', 'stockDisponible', 'caracteristicas']
    
    def get_precio(self, obj):
        if obj.costo:
            return int(obj.costo)
        return 0

    def get_stockDisponible(self, obj):
        inventario = models.InventarioMob.objects.filter(mobiliario=obj, estado_mobil__codigo__in=['DIS', 'DISP', 'DISPO']).first()
        if inventario:
            return int(inventario.cantidad)
        return 0

    def get_caracteristicas(self, obj):
        caracteristicas = obj.descripcion_mob.all()
        nombres = []
        for caracteristica in caracteristicas:
            nombres.append(caracteristica.descripcion)
        return nombres



class MontajeMobiliarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MontajeMobiliario
        fields = '__all__'


# class InventarioMobSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.InventarioMob
#         fields = '__all__'
#         depth = 1

class InventarioMobSerializer(serializers.ModelSerializer):
    # Esto permite que al enviar datos (POST/PATCH) uses IDs, 
    # pero al recibir datos (GET) veas todo el objeto.
    def to_representation(self, instance):
        self.fields['mobiliario'] = MobiliarioSerializer(read_only=True)
        self.fields['estado_mobil'] = EstadoMobilSerializer(read_only=True)
        return super(InventarioMobSerializer, self).to_representation(instance)
    class Meta:
           model = models.InventarioMob
           fields = '__all__'
           # Quita el 'depth = 1' si usas to_representation, es más estable.



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
    tipo_montaje_nombre = serializers.CharField(source='tipo_montaje.nombre', read_only=True)
    montaje_mobiliario = MontajeMobiliarioSerializer(
        source='montajemobiliario_set', 
        many=True, 
        read_only=True
    )

    class Meta:
        model = models.Montaje
        fields = ['id', 'costo', 'salon', 'tipo_montaje', 'tipo_montaje_nombre', 'montaje_mobiliario']

class MobiliariosMontajeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cantidad = serializers.IntegerField()

class ServiciosReservacionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    servicio = serializers.IntegerField(required=False)
    cantidad = serializers.IntegerField(required=False, default=1)
    
    def validate(self, data):
        # Aceptar tanto 'id' como 'servicio'
        if 'servicio' in data and 'id' not in data:
            data['id'] = data['servicio']
        return data

class EquipamientoReservacionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    equipamiento = serializers.IntegerField(required=False)
    cantidad = serializers.IntegerField(required=False, default=1)
    
    def validate(self, data):
        # Aceptar tanto 'id' como 'equipamiento'
        if 'equipamiento' in data and 'id' not in data:
            data['id'] = data['equipamiento']
        return data

class MontajeCreacionSerializer(serializers.Serializer):
    salon = serializers.IntegerField()
    tipo_montaje = serializers.IntegerField()
    mobiliarios = MobiliariosMontajeSerializer(many=True)

class ReservacionCreacionSerializer(serializers.Serializer):
    nombre = serializers.CharField() #
    descripEvento = serializers.CharField(required=False, allow_blank=True, allow_null=True) #
    estimaAsistentes = serializers.IntegerField() #
    fechaEvento = serializers.DateField() #
    horaInicio = serializers.TimeField() #
    horaFin = serializers.TimeField() #
    subtotal = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2, required=False) # no se obtienen xd
    IVA = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2, required=False) # no se obtienen xd
    total = serializers.DecimalField(allow_null=True, max_digits=10, decimal_places=2, required=False) # no se obtienen xd
    cliente = serializers.CharField() #
    trabajador = serializers.CharField(required=False, allow_blank=True) # Allow blank for app
    estado_reserva = serializers.CharField(required=False, allow_blank=True) # Acepta código como string
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


class ReservacionDetalleSerializer(serializers.ModelSerializer):
    """Serializer completo para detalles de reservación del cliente"""
    cliente_datos = serializers.SerializerMethodField()
    montaje_datos = serializers.SerializerMethodField()
    tipo_evento_datos = serializers.SerializerMethodField()
    estado_reserva_datos = serializers.SerializerMethodField()
    servicios = serializers.SerializerMethodField()
    equipamentos = serializers.SerializerMethodField()
    mobiliarios = serializers.SerializerMethodField()

    class Meta:
        model = models.Reservacion
        fields = [
            'id', 'nombreEvento', 'descripEvento', 'fechaReservacion', 'fechaEvento',
            'horaInicio', 'horaFin', 'estimaAsistentes', 'subtotal', 'IVA', 'total',
            'cliente_datos', 'montaje_datos', 'tipo_evento_datos', 'estado_reserva_datos',
            'servicios', 'equipamentos', 'mobiliarios',
            'cliente', 'montaje', 'tipo_evento', 'estado_reserva'
        ]
    
    def get_cliente_datos(self, obj):
        if not obj.cliente:
            return None
        cuenta = obj.cliente.cuenta
        return {
            'nombre': obj.cliente.nombre,
            'apellidoPaterno': obj.cliente.apellidoPaterno,
            'apelidoMaterno': obj.cliente.apelidoMaterno,
            'rfc': obj.cliente.rfc,
            'nombre_fiscal': obj.cliente.nombre_fiscal,
            'telefono': obj.cliente.telefono,
            'dir_colonia': obj.cliente.dir_colonia,
            'dir_calle': obj.cliente.dir_calle,
            'dir_numero': obj.cliente.dir_numero,
            'correo_electronico': cuenta.correo_electronico if cuenta else None,
        }
    
    def get_montaje_datos(self, obj):
        if not obj.montaje:
            return None
        salon = obj.montaje.salon
        tipo_montaje = obj.montaje.tipo_montaje
        return {
            'salon': {
                'nombre': salon.nombre if salon else None,
                'precio': salon.costo if salon else None,
            } if salon else None,
            'tipo_montaje': {
                'nombre': tipo_montaje.nombre if tipo_montaje else None,
            } if tipo_montaje else None,
            'costo': obj.montaje.costo,
            'montaje_mobiliario': [
                {
                    'id': mm.id,
                    'cantidad': mm.cantidad,
                    'nombre': mm.mobiliario.nombre if mm.mobiliario else None,
                    'costo': float(mm.mobiliario.costo) if mm.mobiliario and mm.mobiliario.costo else 0,
                }
                for mm in obj.montaje.montajemobiliario_set.select_related('mobiliario').all()
            ],
        }
    
    def get_tipo_evento_datos(self, obj):
        if not obj.tipo_evento:
            return None
        return {'nombre': obj.tipo_evento.nombre}
    
    def get_estado_reserva_datos(self, obj):
        if not obj.estado_reserva:
            return None
        return {'nombre': obj.estado_reserva.nombre, 'codigo': obj.estado_reserva.codigo}
    
    def get_servicios(self, obj):
        return list(obj.reservaservicio_set.select_related('servicio').values(
            'id', 'servicio__nombre', 'servicio__costo'
        ))
    
    def get_equipamentos(self, obj):
        return list(obj.reservaequipa_set.select_related('equipamiento').values(
            'id', 'cantidad', 'equipamiento__nombre', 'equipamiento__costo'
        ))
    
    def get_mobiliarios(self, obj):
        return []


class ReservacionCoordinadorSerializer(serializers.ModelSerializer):
    """Serializer completo para detalles de reservación del coordinador"""
    cliente_nombre = serializers.CharField(source='cliente.cuenta.nombre_usuario', read_only=True)
    cliente_tipo = serializers.CharField(source='cliente.tipo_cliente.nombre', read_only=True)
    cliente_telefono = serializers.CharField(source='cliente.telefono', read_only=True)
    cliente_email = serializers.CharField(source='cliente.cuenta.correo_electronico', read_only=True)
    cliente_rfc = serializers.CharField(source='cliente.rfc', read_only=True)
    cliente_nombre_fiscal = serializers.CharField(source='cliente.nombre_fiscal', read_only=True)
    cliente_datos = serializers.SerializerMethodField()
    
    salon_nombre = serializers.CharField(source='montaje.salon.nombre', read_only=True)
    montaje_tipo = serializers.CharField(source='montaje.tipo_montaje.nombre', read_only=True)
    montaje_datos = serializers.SerializerMethodField()
    
    estado_nombre = serializers.CharField(source='estado_reserva.nombre', read_only=True)
    estado_codigo = serializers.CharField(source='estado_reserva.codigo', read_only=True)
    tipo_evento_nombre = serializers.CharField(source='tipo_evento.nombre', read_only=True)
    tipo_evento_datos = serializers.SerializerMethodField()
    estado_reserva_datos = serializers.SerializerMethodField()
    
    servicios = serializers.SerializerMethodField()
    equipamentos = serializers.SerializerMethodField()
    mobiliarios = serializers.SerializerMethodField()
    
    # Campos de checklist explícitos
    checklist_coordinador = serializers.JSONField(read_only=True)
    checklist_almacenista = serializers.JSONField(read_only=True)
    progreso_checklist = serializers.FloatField(read_only=True)

    class Meta:
        model = models.Reservacion
        fields = [
            'id', 'nombreEvento', 'descripEvento', 'fechaReservacion', 'fechaEvento',
            'horaInicio', 'horaFin', 'estimaAsistentes', 'subtotal', 'IVA', 'total',
            'cliente_nombre', 'cliente_tipo', 'cliente_telefono', 'cliente_email',
            'cliente_rfc', 'cliente_nombre_fiscal', 'cliente_datos',
            'salon_nombre', 'montaje_tipo', 'montaje_datos',
            'estado_nombre', 'estado_codigo', 'tipo_evento_nombre', 'tipo_evento_datos', 'estado_reserva_datos',
            'servicios', 'equipamentos', 'mobiliarios',
            'checklist_coordinador', 'checklist_almacenista', 'progreso_checklist',
            'cliente', 'montaje', 'tipo_evento', 'estado_reserva'
        ]
    
    def get_cliente_datos(self, obj):
        if not obj.cliente:
            return None
        cuenta = obj.cliente.cuenta
        return {
            'nombre': obj.cliente.nombre,
            'apellidoPaterno': obj.cliente.apellidoPaterno,
            'apelidoMaterno': obj.cliente.apelidoMaterno,
            'rfc': obj.cliente.rfc,
            'nombre_fiscal': obj.cliente.nombre_fiscal,
            'telefono': obj.cliente.telefono,
            'dir_colonia': obj.cliente.dir_colonia,
            'dir_calle': obj.cliente.dir_calle,
            'dir_numero': obj.cliente.dir_numero,
            'correo_electronico': cuenta.correo_electronico if cuenta else None,
        }
    
    def get_montaje_datos(self, obj):
        if not obj.montaje:
            return None
        salon = obj.montaje.salon
        tipo_montaje = obj.montaje.tipo_montaje
        return {
            'salon': {
                'nombre': salon.nombre if salon else None,
                'precio': salon.costo if salon else None,
            } if salon else None,
            'tipo_montaje': {
                'nombre': tipo_montaje.nombre if tipo_montaje else None,
            } if tipo_montaje else None,
            'costo': obj.montaje.costo,
        }
    
    def get_tipo_evento_datos(self, obj):
        if not obj.tipo_evento:
            return None
        return {'nombre': obj.tipo_evento.nombre}
    
    def get_estado_reserva_datos(self, obj):
        if not obj.estado_reserva:
            return None
        return {'nombre': obj.estado_reserva.nombre, 'codigo': obj.estado_reserva.codigo}
    
    def get_servicios(self, obj):
        return list(obj.reservaservicio_set.select_related('servicio').values(
            'id', 'servicio__nombre', 'servicio__costo'
        ))
    
    def get_equipamentos(self, obj):
        return list(obj.reservaequipa_set.select_related('equipamiento').values(
            'id', 'cantidad', 'equipamiento__nombre', 'equipamiento__costo'
        ))
    
    def get_mobiliarios(self, obj):
        if not obj.montaje:
            return []
        return list(obj.montaje.montajemobiliario_set.select_related('mobiliario').values(
            'id', 'cantidad', 'mobiliario__nombre', 'mobiliario__costo'
        ))


class ReservacionUpdateSerializer(serializers.Serializer):
    nombreEvento = serializers.CharField(required=False)
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


class DisponibilidadSalonSerializer(serializers.ModelSerializer):
    salon_nombre = serializers.CharField(source='montaje.salon.nombre', read_only=True)
    tipo_evento_nombre = serializers.CharField(source='tipo_evento.nombre', read_only=True)
    
    class Meta:
        model = models.Reservacion
        fields = ['id', 'nombreEvento', 'fechaEvento', 'horaInicio', 'horaFin', 'salon_nombre', 'tipo_evento_nombre']


class ReservacionResumenSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    salon_nombre = serializers.CharField(source='montaje.salon.nombre', read_only=True)
    estado_nombre = serializers.CharField(source='estado_reserva.nombre', read_only=True)
    estado_codigo = serializers.CharField(source='estado_reserva.codigo', read_only=True)
    
    class Meta:
        model = models.Reservacion
        fields = ['id', 'nombreEvento', 'fechaEvento', 'horaInicio', 'horaFin', 
                  'cliente_nombre', 'salon_nombre', 'estado_nombre', 'estado_codigo', 'total']


class ReservacionFormularioSerializer(serializers.ModelSerializer):
    cliente_rfc = serializers.CharField(source='cliente.rfc', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    cliente_apellido = serializers.CharField(source='cliente.apellidoPaterno', read_only=True)
    cliente_correo = serializers.CharField(source='cliente.cuenta.correo_electronico', read_only=True)
    cliente_telefono = serializers.CharField(source='cliente.telefono', read_only=True)
    cliente_nombre_fiscal = serializers.CharField(source='cliente.nombre_fiscal', read_only=True)
    salon_id = serializers.IntegerField(source='montaje.salon.id', read_only=True)
    salon_nombre = serializers.CharField(source='montaje.salon.nombre', read_only=True)
    tipo_montaje_id = serializers.IntegerField(source='montaje.tipo_montaje.id', read_only=True)
    tipo_montaje_nombre = serializers.CharField(source='montaje.tipo_montaje.nombre', read_only=True)
    
    cliente = serializers.SerializerMethodField()
    servicios = serializers.SerializerMethodField()
    equipamentos = serializers.SerializerMethodField()
    mobiliarios = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Reservacion
        fields = [
            'id', 'nombreEvento', 'descripEvento', 'fechaEvento', 'horaInicio', 'horaFin',
            'estimaAsistentes', 'subtotal', 'IVA', 'total',
            'cliente_rfc', 'cliente_nombre', 'cliente_apellido', 'cliente_correo', 'cliente_telefono', 'cliente_nombre_fiscal',
            'salon_id', 'salon_nombre', 'tipo_montaje_id', 'tipo_montaje_nombre',
            'tipo_evento',
            'cliente', 'servicios', 'equipamentos', 'mobiliarios'
        ]
    
    def get_cliente(self, obj):
        return {
            'correo': obj.cliente.cuenta.correo_electronico if obj.cliente.cuenta else None,
            'telefono': obj.cliente.telefono,
            'nombre_fiscal': obj.cliente.nombre_fiscal
        }
    
    def get_servicios(self, obj):
        return list(obj.reservaservicio_set.values_list('servicio__nombre', flat=True))
    
    def get_equipamentos(self, obj):
        return [
            re.equipamiento.nombre for re in obj.reservaequipa_set.all()
        ]
    
    def get_mobiliarios(self, obj):
        return [
            mm.mobiliario.nombre for mm in obj.montaje.montajemobiliario_set.all()
        ]


class ReservacionProgresoSerializer(serializers.Serializer):
    """Serializer para devolver solo el progreso del checklist"""
    id = serializers.IntegerField()
    nombreEvento = serializers.CharField()
    fechaEvento = serializers.DateField()
    horaInicio = serializers.TimeField()
    horaFin = serializers.TimeField()
    progreso_checklist = serializers.FloatField()
    checklist_coordinador = serializers.JSONField()
    estado_reserva_datos = serializers.SerializerMethodField()
    
    def get_estado_reserva_datos(self, obj):
        if not obj.estado_reserva:
            return None
        return {'nombre': obj.estado_reserva.nombre, 'codigo': obj.estado_reserva.codigo}


class PaqueteSerializer(serializers.ModelSerializer):
    salon_nombre = serializers.CharField(source='montaje.salon.nombre', read_only=True)
    salon_id = serializers.IntegerField(source='montaje.salon.id', read_only=True)
    salon_precio = serializers.IntegerField(source='montaje.salon.costo', read_only=True)
    salon_capacidad = serializers.IntegerField(source='montaje.salon.maxCapacidad', read_only=True)
    salon_metros = serializers.IntegerField(source='montaje.salon.metrosCuadrados', read_only=True)
    salon_ubicacion = serializers.CharField(source='montaje.salon.ubicacion', read_only=True)
    montaje_nombre = serializers.CharField(source='montaje.tipo_montaje.nombre', read_only=True)
    montaje_id = serializers.IntegerField(source='montaje.id', read_only=True)
    
    servicios = serializers.SerializerMethodField()
    equipamentos = serializers.SerializerMethodField()
    mobiliarios = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Reservacion
        fields = [
            'id', 'nombre_paquete', 'descripEvento',
            'subtotal', 'IVA', 'total',
            'salon_id', 'salon_nombre', 'salon_precio', 'salon_capacidad',
            'salon_metros', 'salon_ubicacion',
            'montaje_id', 'montaje_nombre',
            'servicios', 'equipamentos', 'mobiliarios',
        ]
    
    def get_servicios(self, obj):
        return [
            {
                'id': rs.servicio.id,
                'nombre': rs.servicio.nombre,
                'costo': int(rs.servicio.costo),
                'precio': int(rs.servicio.costo),
                'tipo': rs.servicio.tipo_servicio.nombre if rs.servicio.tipo_servicio else '',
            }
            for rs in obj.reservaservicio_set.select_related('servicio__tipo_servicio').all()
        ]
    
    def get_equipamentos(self, obj):
        return [
            {
                'id': re.equipamiento.id,
                'nombre': re.equipamiento.nombre,
                'costo': int(re.equipamiento.costo),
                'precio': int(re.equipamiento.costo),
                'cantidad': re.cantidad,
                'tipo': re.equipamiento.tipo_equipa.nombre if re.equipamiento.tipo_equipa else '',
            }
            for re in obj.reservaequipa_set.select_related('equipamiento__tipo_equipa').all()
        ]
    
    def get_mobiliarios(self, obj):
        if not obj.montaje:
            return []
        return [
            {
                'id': mm.mobiliario.id,
                'nombre': mm.mobiliario.nombre,
                'costo': int(mm.mobiliario.costo),
                'precio': int(mm.mobiliario.costo),
                'cantidad': mm.cantidad,
                'tipo': mm.mobiliario.tipo_movil.nombre if mm.mobiliario.tipo_movil else '',
            }
            for mm in obj.montaje.montajemobiliario_set.select_related('mobiliario__tipo_movil').all()
        ]