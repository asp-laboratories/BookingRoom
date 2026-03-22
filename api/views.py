from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from BookingRoomApp.models import TipoServicio, Cuenta, Trabajador, Rol, EstadoCuenta, TipoCliente, DatosCliente, TipoEquipa
from .serializers import (
    TipoServicioSerializer, RolSerializer, EstadoCuentaSerializer,
    TipoClienteSerializer, CuentaSerializer, CuentaMinimalSerializer,
    TrabajadorSerializer, DatosClienteSerializer, LoginResponseSerializer, TipoEquipaSerializer
)
import json

try:
    import firebase_admin
    from firebase_admin import auth
    FIREBASE_ENABLED = True
except:
    FIREBASE_ENABLED = False


class ListTipoEquipa(APIView):
    def get(self, request):
        tipo_equipa = TipoEquipa.objects.all()
        serializer = TipoEquipaSerializer(tipo_equipa, many=True)
        return Response(serializer.data)

class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer


class EstadoCuentaViewSet(viewsets.ModelViewSet):
    queryset = EstadoCuenta.objects.all()
    serializer_class = EstadoCuentaSerializer


class TipoClienteViewSet(viewsets.ModelViewSet):
    queryset = TipoCliente.objects.all()
    serializer_class = TipoClienteSerializer


class CuentaViewSet(viewsets.ModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer


class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = Trabajador.objects.select_related('rol', 'cuenta').all()
    serializer_class = TrabajadorSerializer


class DatosClienteViewSet(viewsets.ModelViewSet):
    queryset = DatosCliente.objects.select_related('tipo_cliente', 'cuenta').all()
    serializer_class = DatosClienteSerializer


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
                cuenta = Cuenta.objects.get(firebase_uid=firebase_uid)
            except Cuenta.DoesNotExist:
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
                cuenta = Cuenta.objects.get(firebase_uid=firebase_uid)
            except Cuenta.DoesNotExist:
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
                trabajador = Trabajador.objects.select_related('rol').get(cuenta_id=cuenta.id)
                user_data['tipo'] = 'trabajador'
                user_data['rol'] = trabajador.rol.codigo
                user_data['nombre'] = trabajador.nombre
            except Trabajador.DoesNotExist:
                pass
            
            serializer = LoginResponseSerializer(user_data)
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
            
            estado_cuenta = EstadoCuenta.objects.filter(codigo='ACT').first()
            
            cuenta, created = Cuenta.objects.get_or_create(
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
