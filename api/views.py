from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from BookingRoomApp import models
from . import serializers, services
import json

try:
    import firebase_admin
    from firebase_admin import auth
    FIREBASE_ENABLED = True
except:
    FIREBASE_ENABLED = False


class ListTipoEquipa(APIView):
    def get(self, request):
        tipo_equipa = models.TipoEquipa.objects.all()
        serializer = serializers.TipoEquipaSerializer(tipo_equipa, many=True)
        return Response(serializer.data)


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = models.TipoServicio.objects.all()
    serializer_class = serializers.TipoServicioSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset = models.Rol.objects.all()
    serializer_class = serializers.RolSerializer


class EstadoCuentaViewSet(viewsets.ModelViewSet):
    queryset = models.EstadoCuenta.objects.all()
    serializer_class = serializers.EstadoCuentaSerializer


class TipoClienteViewSet(viewsets.ModelViewSet):
    queryset = models.TipoCliente.objects.all()
    serializer_class = serializers.TipoClienteSerializer


class CuentaViewSet(viewsets.ModelViewSet):
    queryset = models.Cuenta.objects.all()
    serializer_class = serializers.CuentaSerializer


class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = models.Trabajador.objects.select_related('rol', 'cuenta').all()
    serializer_class = serializers.TrabajadorSerializer


class DatosClienteViewSet(viewsets.ModelViewSet):
    queryset = models.DatosCliente.objects.select_related('tipo_cliente', 'cuenta').all()
    serializer_class = serializers.DatosClienteSerializer

class MobiliarioViewSet(viewsets.ModelViewSet):
    queryset = models.Mobiliario.objects.all()
    serializer_class = serializers.MobiliarioSerializer

class InventarioMobViewSet(viewsets.ModelViewSet):
    queryset = models.InventarioMob.objects.all()
    serializer_class = serializers.InventarioMobSerializer

class CaracterMobilViewSet(viewsets.ModelViewSet):
    queryset = models.CaracterMobil.objects.all()
    serializer_class = serializers.CaracterMobilSerializer

class SalonViewSet(viewsets.ModelViewSet):
    queryset = models.Salon.objects.all()
    serializer_class = serializers.SalonSerializer

class RegistrEstadSalonViewSet(viewsets.ModelViewSet):
    queryset = models.RegistrEstadSalon.objects.all()
    serializer_class = serializers.RegistrEstadSalonSerializer

class MontajeViewSet(viewsets.ModelViewSet):
    queryset = models.Montaje.objects.all()
    serializer_class = serializers.MontajeSerializer

class MontajeMobiliarioViewSet(viewsets.ModelViewSet):
    queryset = models.MontajeMobiliario.objects.all()
    serializer_class = serializers.MontajeMobiliarioSerializer

class ReservacionViewSet(viewsets.ModelViewSet):
    queryset = models.Reservacion.objects.all()
    serializer_class = serializers.ReservacionSerializer




@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            if not token:
                return JsonResponse({'error': 'Token requerido'}, status=400)
            
            if not FIREBASE_ENABLED:
                return JsonResponse({'error': 'Firebase no configurado'}, status=500)
            
            if len(token) > 10000:
                return JsonResponse({'error': 'Token inválido'}, status=400)
            
            decoded = auth.verify_id_token(token)
            firebase_uid = decoded['uid']
            email = decoded.get('email', '')
            
            try:
                cuenta = models.Cuenta.objects.get(firebase_uid=firebase_uid)
            except models.Cuenta.DoesNotExist:
                return JsonResponse({'error': 'Cuenta no registrada en el sistema'}, status=404)
            
            request.session['cuenta_id'] = cuenta.id
            request.session['firebase_uid'] = firebase_uid
            request.session.modified = True
            
            return JsonResponse({'success': True, 'user': {
                'id': cuenta.id,
                'nombre': cuenta.nombre_usuario,
                'email': cuenta.correo_electronico
            }})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def api_flutter_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            if not token:
                return JsonResponse({'error': 'Token requerido'}, status=400)
            
            if not FIREBASE_ENABLED:
                return JsonResponse({'error': 'Firebase no configurado'}, status=500)
            
            if len(token) > 10000:
                return JsonResponse({'error': 'Token inválido'}, status=400)
            
            decoded = auth.verify_id_token(token)
            firebase_uid = decoded['uid']
            
            try:
                cuenta = models.Cuenta.objects.get(firebase_uid=firebase_uid)
            except models.Cuenta.DoesNotExist:
                return JsonResponse({'error': 'Cuenta no registrada en el sistema'}, status=404)
            
            request.session['cuenta_id'] = cuenta.id
            request.session['firebase_uid'] = firebase_uid
            request.session.modified = True
            
            user_data = {
                'id': cuenta.id,
                'nombre': cuenta.nombre_usuario,
                'email': cuenta.correo_electronico,
                'tipo': 'cliente',
                'rol': None
            }
            
            try:
                trabajador = models.Trabajador.objects.select_related('rol').get(cuenta_id=cuenta.id)
                user_data['tipo'] = 'trabajador'
                user_data['rol'] = trabajador.rol.codigo
                user_data['nombre'] = trabajador.nombre
            except models.Trabajador.DoesNotExist:
                pass
            
            serializer = serializers.LoginResponseSerializer(user_data)
            return JsonResponse({'success': True, 'user': serializer.data})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
def api_signup(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            if not token:
                return JsonResponse({'error': 'Token requerido'}, status=400)
            
            if not FIREBASE_ENABLED:
                return JsonResponse({'error': 'Firebase no configurado'}, status=500)
            
            if len(token) > 10000:
                return JsonResponse({'error': 'Token inválido'}, status=400)
            
            decoded = auth.verify_id_token(token)
            firebase_uid = decoded['uid']
            email = decoded.get('email', '')
            display_name = decoded.get('name', '')
            
            estado_cuenta = models.EstadoCuenta.objects.filter(codigo='ACT').first()
            
            cuenta, created = models.Cuenta.objects.get_or_create(
                firebase_uid=firebase_uid,
                defaults={
                    'nombre_usuario': display_name,
                    'correo_electronico': email,
                    'estado_cuenta': estado_cuenta,
                    'disposicion': True
                }
            )
            
            if created:
                return JsonResponse({'success': True, 'message': 'Cuenta creada exitosamente'})
            else:
                return JsonResponse({'success': True, 'message': 'Ya tenías una cuenta'})
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)
