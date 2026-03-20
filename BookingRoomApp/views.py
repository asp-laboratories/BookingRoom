from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .models import TipoServicio, Cuenta, Trabajador, Rol, EstadoCuenta
from .serializers import TipoServicioSerializer
import json

try:
    import firebase_admin
    from firebase_admin import auth
    FIREBASE_ENABLED = True
except:
    FIREBASE_ENABLED = False


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = TipoServicio.objects.all()
    serializer_class = TipoServicioSerializer


def login(request):
    return render(request, 'BookingRoomApp/login.html')


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
            
            # Verificar token con Firebase
            decoded = auth.verify_id_token(token)
            firebase_uid = decoded['uid']
            email = decoded.get('email', '')
            
            # Buscar o crear sesión en BD local
            try:
                cuenta = Cuenta.objects.get(firebase_uid=firebase_uid)
            except Cuenta.DoesNotExist:
                return JsonResponse({'error': 'Cuenta no registrada en el sistema'}, status=404)
            
            # Guardar sesión en Django
            request.session['cuenta_id'] = cuenta.id
            request.session['firebase_uid'] = firebase_uid
            
            return JsonResponse({'success': True, 'user': {
                'id': cuenta.id,
                'nombre': cuenta.nombre_usuario,
                'email': cuenta.correo_electronico
            }})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def sign_up(request):
    return render(request, 'BookingRoomApp/sign_up.html')


def home(request):
    cuenta_id = request.session.get('cuenta_id')
    
    if not cuenta_id:
        return HttpResponseRedirect(reverse('login'))
    
    cuenta = Cuenta.objects.get(id=cuenta_id)
    
    return render(request, 'BookingRoomApp/home.html', {
        'cuenta': cuenta
    })


def reservacion(request):
    tipos_servicio = TipoServicio.objects.filter(disposicion=True)
    return render(request, 'BookingRoomApp/reservacion.html', {'tipos_servicio': tipos_servicio})


def servicios(request):
    return render(request, 'BookingRoomApp/administracion/servicios.html')


def trabajadores(request):
    roles = Rol.objects.all()
    trabajadores_list = Trabajador.objects.select_related('cuenta', 'rol').all()
    
    return render(request, 'BookingRoomApp/administracion/trabajadores.html', {
        'roles': roles,
        'trabajadores': trabajadores_list
    })


def registrar_trabajador(request):
    estado_cuenta = EstadoCuenta.objects.filter(codigo='ACT').first()
    
    if request.method == 'POST':
        form_tipo = request.POST.get('form_tipo')
        
        if form_tipo == 'cuenta':
            nombre_usuario = request.POST.get('nombre_usuario')
            email = request.POST.get('email')
            contrasena = request.POST.get('contrasena')
            confirmar_contrasena = request.POST.get('confirmar_contrasena')
            
            if contrasena != confirmar_contrasena:
                messages.error(request, 'Las contraseñas no coinciden')
                return HttpResponseRedirect(reverse('trabajadores'))
            
            request.session['cuenta_data'] = {
                'nombre_usuario': nombre_usuario,
                'email': email,
                'contrasena': contrasena,
            }
            messages.success(request, 'Datos de cuenta guardados. Complete los datos del trabajador para poder registrarlo en el sitema.')
            return HttpResponseRedirect(reverse('trabajadores'))
        
        elif form_tipo == 'trabajador':
            cuenta_data = request.session.get('cuenta_data')
            if not cuenta_data:
                messages.error(request, 'Primero complete los datos de la cuenta')
                return HttpResponseRedirect(reverse('trabajadores'))
            
            no_empleado = request.POST.get('no_empleado')
            rfc = request.POST.get('rfc')
            nombre = request.POST.get('nombre')
            apellido_paterno = request.POST.get('apellido_paterno')
            apellido_materno = request.POST.get('apellido_materno')
            telefono = request.POST.get('telefono')
            rol_id = request.POST.get('rol_id')
            
            try:
                firebase_uid = None
                if FIREBASE_ENABLED:
                    try:
                        firebase_user = auth.create_user(
                            email=cuenta_data['email'],
                            password=cuenta_data['contrasena'],
                            display_name=cuenta_data['nombre_usuario']
                        )
                        firebase_uid = firebase_user.uid
                    except Exception as e:
                        messages.warning(request, f'Firebase no disponible: {str(e)}')

                cuenta = Cuenta.objects.create(
                    nombre_usuario=cuenta_data['nombre_usuario'],
                    correo_electronico=cuenta_data['email'],
                    firebase_uid=firebase_uid,
                    estado_cuenta=estado_cuenta,
                    disposicion=True
                )

                Trabajador.objects.create(
                    no_empleado=no_empleado,
                    rfc=rfc,
                    nombre_fiscal=f"{nombre} {apellido_paterno} {apellido_materno}",
                    nombre=nombre,
                    apellidoPaterno=apellido_paterno,
                    apelidoMaterno=apellido_materno,
                    telefono=telefono,
                    correo_electronico=cuenta_data['email'],
                    rol_id=rol_id,
                    cuenta=cuenta
                )

                del request.session['cuenta_data']
                messages.success(request, 'Trabajador registrado exitosamente')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                if FIREBASE_ENABLED and firebase_uid:
                    try:
                        auth.delete_user(firebase_uid)
                    except:
                        pass
    
    return HttpResponseRedirect(reverse('trabajadores'))


def salones(request):
    return render(request, 'BookingRoomApp/administracion/salones.html')


def mobiliario(request):
    return render(request, 'BookingRoomApp/administracion/mobiliario.html')


def equipamiento(request):
    return render(request, 'BookingRoomApp/administracion/equipamiento.html')


def historial_reservacion(request):
    return render(request, 'BookingRoomApp/recepcion/historial_reservacion.html')


def inventario_equipamiento(request):
    return render(request, 'BookingRoomApp/almacen/inventario_equipamiento.html')


def inventario_mobiliario(request):
    return render(request, 'BookingRoomApp/almacen/inventario_mobiliario.html')


def pagos(request):
    return render(request, 'BookingRoomApp/recepcion/pagos.html')


def estadisticas(request):
    return render(request, 'BookingRoomApp/administracion/estadisticas.html')
