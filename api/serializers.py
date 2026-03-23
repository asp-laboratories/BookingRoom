from rest_framework import serializers
from django.contrib.auth.models import User
from BookingRoomApp.models import TipoServicio, Rol, EstadoCuenta, TipoCliente, Cuenta, Trabajador, DatosCliente, TipoEquipa


class TipoEquipaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipa
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
        model = TipoServicio
        fields = '__all__'


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'


class EstadoCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCuenta
        fields = '__all__'


class TipoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCliente
        fields = '__all__'


class CuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = '__all__'


class CuentaMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuenta
        fields = ['id', 'nombre_usuario', 'correo_electronico']


class TrabajadorSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)
    rol_codigo = serializers.CharField(source='rol.codigo', read_only=True)
    cuenta_nombre = serializers.CharField(source='cuenta.nombre_usuario', read_only=True)
    
    class Meta:
        model = Trabajador
        fields = '__all__'


class DatosClienteSerializer(serializers.ModelSerializer):
    tipo_cliente_nombre = serializers.CharField(source='tipo_cliente.nombre', read_only=True)
    cuenta_nombre = serializers.CharField(source='cuenta.nombre_usuario', read_only=True)
    
    class Meta:
        model = DatosCliente
        fields = '__all__'


class LoginResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    email = serializers.EmailField()
    tipo = serializers.CharField()
    rol = serializers.CharField(allow_null=True)
