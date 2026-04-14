from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from BookingRoomApp import models
from . import serializers
from .services import montajeService, reservacionesService
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
        tipo_equipa = models.TipoEquipa.objects.all()
        serializer = serializers.TipoEquipaSerializer(tipo_equipa, many=True)
        return Response(serializer.data)


class TipoServicioViewSet(viewsets.ModelViewSet):
    queryset = models.TipoServicio.objects.all()
    serializer_class = serializers.TipoServicioSerializer
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


class TipoMontajeViewSet(viewsets.ModelViewSet):
    queryset = models.TipoMontaje.objects.all()
    serializer_class = serializers.TipoMontajeSerializer


class TipoMobilViewSet(viewsets.ModelViewSet):
    queryset = models.TipoMobil.objects.all()
    serializer_class = serializers.TipoMobilSerializer


class TipoEventoViewSet(viewsets.ModelViewSet):
    queryset = models.TipoEvento.objects.all()
    serializer_class = serializers.TipoEventoSerializer


class CuentaViewSet(viewsets.ModelViewSet):
    queryset = models.Cuenta.objects.all()
    serializer_class = serializers.CuentaSerializer


class TrabajadorViewSet(viewsets.ModelViewSet):
    queryset = models.Trabajador.objects.select_related('rol', 'cuenta').all()
    serializer_class = serializers.TrabajadorSerializer


class DatosClienteViewSet(viewsets.ModelViewSet):
    queryset = models.DatosCliente.objects.select_related('tipo_cliente', 'cuenta').all()
    serializer_class = serializers.DatosClienteSerializer

    def get_queryset(self):
        correo = self.request.query_params.get('correo')
        if correo:
            return self.queryset.filter(correo_electronico=correo)
        return super().get_queryset()


class MobiliarioViewSet(viewsets.ModelViewSet):
    queryset = models.Mobiliario.objects.select_related('tipo_movil').all()
    serializer_class = serializers.MobiliarioSerializer


class InventarioMobViewSet(viewsets.ModelViewSet):
    queryset = models.InventarioMob.objects.all()
    serializer_class = serializers.InventarioMobSerializer


class CaracterMobilViewSet(viewsets.ModelViewSet):
    queryset = models.CaracterMobil.objects.all()
    serializer_class = serializers.CaracterMobilSerializer


class SalonViewSet(viewsets.ModelViewSet):
    queryset = models.Salon.objects.select_related('estado_salon').all()

    def get_serializer_class(self):
        return serializers.SalonSerializer

    def get_queryset(self):
        return models.Salon.objects.select_related('estado_salon').all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        from django.utils import timezone
        fecha_hoy = timezone.now().date()
        
        data = serializer.data
        for i, salon_data in enumerate(data):
            salon = queryset[i]
            
            # Obtener el registro de HOY
            registro_hoy = models.RegistrEstadSalon.objects.filter(
                salon=salon,
                fecha=fecha_hoy
            ).select_related('estado_salon').first()
            
            if registro_hoy:
                salon_data['estado'] = registro_hoy.estado_salon.nombre
                salon_data['estado_codigo'] = registro_hoy.estado_salon.codigo
            else:
                # Si no hay registro hoy, usar estado actual del salon
                if salon.estado_salon:
                    salon_data['estado'] = salon.estado_salon.nombre
                    salon_data['estado_codigo'] = salon.estado_salon.codigo
                else:
                    salon_data['estado'] = 'Disponible'
                    salon_data['estado_codigo'] = 'DIS'
        
        return Response(data)

    def update(self, request, *args, **kwargs):
        import logging
        from django.utils import timezone
        from datetime import datetime
        
        logger = logging.getLogger(__name__)
        
        salon = self.get_object()
        print(f"DEBUG UPDATE: salon={salon.nombre}, old estado={salon.estado_salon}")
        nuevo_estado_input = request.data.get('estado_salon')
        fecha_input = request.data.get('fecha')
        print(f"DEBUG UPDATE: nuevo_estado_input={nuevo_estado_input}")
        print(f"DEBUG UPDATE: fecha_input={fecha_input}")
        
        # Procesar la fecha
        if fecha_input:
            try:
                fecha_registro = datetime.fromisoformat(fecha_input.replace('Z', '+00:00')).date()
            except:
                fecha_registro = timezone.now().date()
        else:
            fecha_registro = timezone.now().date()
        
        fecha_hoy = timezone.now().date()
        
        if nuevo_estado_input:
            # Mapeo de códigos Flutter a códigos DB
            codigo_map = {
                'DISP': 'DIS',
                'LIM': 'LIMPI',
                'LIMPIEZA': 'LIMPI',
                'NODISP': 'NODIS',
                'RESV': 'RESV',
                'DISPONIBLE': 'DIS',
                'NO_DISPONIBLE': 'NODIS',
                'RESERVADO': 'RESV',
                'MANTE': 'MANTE',
                'MANTENIMIENTO': 'MANTE',
                'OCUP': 'OCUP',
                'OCUPADO': 'OCUP',
            }
            
            codigo_buscar = codigo_map.get(nuevo_estado_input.upper(), nuevo_estado_input.upper())
            print(f"DEBUG UPDATE: codigo_buscar={codigo_buscar}")
            
            # Verificar si se intenta cambiar a Limpieza y el salon está ocupado/reservado hoy
            if codigo_buscar == 'LIMPI':
                registro_hoy = models.RegistrEstadSalon.objects.filter(
                    salon=salon,
                    fecha=fecha_hoy
                ).select_related('estado_salon').first()
                
                if registro_hoy and registro_hoy.estado_salon.codigo in ('RESV', 'OCUP'):
                    return Response(
                        {'error': 'No se puede cambiar a Limpieza: salon ocupado/reservado hoy'},
                        status=400
                    )
            
            try:
                nuevo_estado = models.EstadoSalon.objects.get(codigo=codigo_buscar)
                print(f"DEBUG UPDATE: nuevo_estado encontrado={nuevo_estado.nombre} (codigo={nuevo_estado.codigo})")
                
                salon.estado_salon = nuevo_estado
                salon.save()
                print(f"DEBUG UPDATE: salon.save() completado")
                
                # Verificar estados existentes
                todos_estados = models.EstadoSalon.objects.all()
                print(f"DEBUG UPDATE: Todos los estados en DB: {[(e.nombre, e.codigo) for e in todos_estados]}")
                
                registro = models.RegistrEstadSalon.objects.create(
                    salon=salon,
                    estado_salon=nuevo_estado,
                    fecha=fecha_registro
                )
                print(f"DEBUG UPDATE: registro creado id={registro.id}, fecha={fecha_registro}")
                
                # Verificar que se creó
                ultimos = models.RegistrEstadSalon.objects.filter(salon=salon).order_by('-id')[:3]
                print(f"DEBUG UPDATE: Últimos registros para salon {salon.id}: {[(r.estado_salon.nombre, str(r.fecha)) for r in ultimos]}")
                
                # Devolver en formato consistente con list
                return Response({
                    'id': salon.id,
                    'nombre': salon.nombre,
                    'estado': nuevo_estado.nombre,
                    'estado_codigo': nuevo_estado.codigo,
                })
                    
            except models.EstadoSalon.DoesNotExist:
                # Si no existe el código, buscar cualquier estado disponible
                nuevo_estado = models.EstadoSalon.objects.first()
                if nuevo_estado:
                    salon.estado_salon = nuevo_estado
                    salon.save()
                    models.RegistrEstadSalon.objects.create(
                        salon=salon,
                        estado_salon=nuevo_estado
                    )
                    return Response({
                        'id': salon.id,
                        'nombre': salon.nombre,
                        'estado': nuevo_estado.nombre,
                        'estado_codigo': nuevo_estado.codigo,
                    })
                return Response({'error': 'No hay estados de salón configurados'}, status=400)
        
        return super().update(request, *args, **kwargs)


class RegistrEstadSalonViewSet(viewsets.ModelViewSet):
    queryset = models.RegistrEstadSalon.objects.all()
    serializer_class = serializers.RegistrEstadSalonSerializer

    # TODO: Descomentar cuando se ejecute migración para agregar campo fecha_fin
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     fecha = self.request.query_params.get('fecha')
    #     
    #     if fecha:
    #         from datetime import datetime
    #         try:
    #             fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()
    #             queryset = models.RegistrEstadSalon.objects.filter(
    #                 fecha__lte=fecha_dt
    #             ).select_related('salon', 'estado_salon').order_by('salon', '-fecha')
    #             
    #             seen = set()
    #             unique_queryset = []
    #             for item in queryset:
    #                 if item.salon_id not in seen:
    #                     seen.add(item.salon_id)
    #                     unique_queryset.append(item)
    #             return unique_queryset
    #         except ValueError:
    #             pass
    #     
    #     return queryset.select_related('salon', 'estado_salon').order_by('salon', '-fecha')


class ReservaServicioViewSet(viewsets.ModelViewSet):
    queryset = models.ReservaServicio.objects.all()
    serializer_class = serializers.ReservaServicioSerializer


# la logica de este view set se repite en varias zonas
class MontajeViewSet(viewsets.ModelViewSet):
    queryset = models.Montaje.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            # para creacion personalizada, entrada de datos en tabla motanej mobiliario
            return serializers.MontajeCreacionSerializer
        
        if self.action in ['list', 'retrieve']:
            return serializers.MontajeLecturaSerializer
        
        # serializer normalito par demas accionesaparte de crear
        return serializers.MontajeSerializer

    # se sobrescribe la creacion de acuerdo a lo q queremos q haga
    def create(self, request, *args, **kwargs):
        validador = self.get_serializer(data=request.data)
        validador.is_valid(raise_exception=True)

        try:
            new_montaje = montajeService.crear_montaje(validador.validated_data)
            respuesta = serializers.MontajeSerializer(new_montaje)
            return Response(respuesta.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MontajeMobiliarioViewSet(viewsets.ModelViewSet):
    queryset = models.MontajeMobiliario.objects.all()
    serializer_class = serializers.MontajeMobiliarioSerializer


class ReservacionViewSet(viewsets.ModelViewSet):
    queryset = models.Reservacion.objects.select_related('cliente', 'montaje', 'estado_reserva', 'tipo_evento', 'trabajador')

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.ReservacionCreacionSerializer
        
        if self.action == 'retrieve':
            return serializers.ReservacionDetalleSerializer
        
        if self.action in ['list']:
            return serializers.ReservacionLecturaSerializer
        
        if self.action in ['update', 'partial_update']:
            return serializers.ReservacionUpdateSerializer
        
        return serializers.ReservacionSerializer
    
    def perform_update(self, serializer):
        cambio_reservacion = serializer.validated_data
        original = serializer.instance
        
        if 'estado_reserva' in cambio_reservacion:
            nuevo_estado = cambio_reservacion.pop('estado_reserva')
            if nuevo_estado != original.estado_reserva:
                reservacionesService.cambio_estado_reservacion(original, nuevo_estado)

        reservacionesService.modificacion_aditamentos(original=original, nuevos_datos=cambio_reservacion)

    def create(self, request, *args, **kwargs):
        validador = self.get_serializer(data=request.data)
        validador.is_valid(raise_exception=True)

        try:
            confirmar = request.data.get('confirmar_inventario', True)
            new_reservacion = reservacionesService.crear_reservacion(validador.validated_data, confirmar_inventario=confirmar)
            respeusta = serializers.ReservacionLecturaSerializer(new_reservacion)
            return Response(respeusta.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            error_str = str(e)
            # Intentar parsear el error como dict
            if error_str.startswith('{') and error_str.endswith('}'):
                try:
                    import json
                    error_data = eval(error_str)
                    if isinstance(error_data, dict):
                        return Response({'error': [error_data]}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    pass
            return Response({"error": [error_str]}, status=status.HTTP_400_BAD_REQUEST)




class EncuestaViewSet(viewsets.ModelViewSet):
    queryset = models.Encuesta.objects.select_related('reservacion').all()
    serializer_class = serializers.EncuestaSerializer


class RegistrEstadReservaViewSet(viewsets.ModelViewSet):
    queryset = models.RegistrEstadReserva.objects.select_related('reservacion', 'estado_reserva').all()
    serializer_class = serializers.RegistrEstadReservaSerializer


class EquipamientoViewSet(viewsets.ModelViewSet):
    queryset = models.Equipamiento.objects.select_related('tipo_equipa').all()
    serializer_class = serializers.EquipamientoSerializer


class InventarioEquipaViewSet(viewsets.ModelViewSet):
    queryset = models.InventarioEquipa.objects.select_related('equipamiento', 'estado_equipa').all()
    serializer_class = serializers.InventarioEquipaSerializer


class ReservaEquipaViewSet(viewsets.ModelViewSet):
    queryset = models.ReservaEquipa.objects.select_related('reservacion', 'equipamiento').all()
    serializer_class = serializers.ReservaEquipaSerializer


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = models.Servicio.objects.select_related('tipo_servicio').all()
    serializer_class = serializers.ServicioSerializer


class PagoViewSet(viewsets.ModelViewSet):
    queryset = models.Pago.objects.select_related('metodo_pago', 'concepto_pago', 'reservacion').all()
    serializer_class = serializers.PagoSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Al crear un pago, cambiar el estado de la reservación a 'CON' (Confirmada)
        """
        from django.db import transaction
        
        with transaction.atomic():
            # Obtener la reservación antes de crear el pago
            reservacion_id = request.data.get('reservacion') or request.data.get('reservacion_id')
            
            if not reservacion_id:
                return Response({'error': 'Reservación requerida'}, status=400)
            
            try:
                reservacion = models.Reservacion.objects.get(pk=reservacion_id)
                
                # Cambiar estado a 'CON' (Confirmada) cuando se realiza un pago
                estado_confirmado = models.EstadoReserva.objects.filter(codigo='CON').first()
                if estado_confirmado and reservacion.estado_reserva.codigo != 'CON':
                    reservacion.estado_reserva = estado_confirmado
                    reservacion.save(update_fields=['estado_reserva'])
                    
                    # Registrar el cambio de estado
                    models.RegistrEstadReserva.objects.create(
                        reservacion=reservacion,
                        estado_reserva=estado_confirmado
                    )
            except models.Reservacion.DoesNotExist:
                return Response({'error': 'Reservación no encontrada'}, status=404)
            
            # Crear el pago normalmente
            return super().create(request, *args, **kwargs)


class BuscarReservacionView(APIView):
    def get(self, request):
        numero = request.GET.get('numero')
        if not numero:
            return Response({'error': 'Número de reservación requerido'}, status=400)
        
        try:
            reservacion = models.Reservacion.objects.select_related(
                'cliente', 'estado_reserva'
            ).get(pk=numero)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)
        
        pagos_count = models.Pago.objects.filter(reservacion=reservacion).count()
        ultimo_pago = models.Pago.objects.filter(reservacion=reservacion).order_by('-no_pago').first()
        
        if ultimo_pago:
            saldo = ultimo_pago.saldo
        else:
            saldo = reservacion.total
        
        return Response({
            'id': reservacion.id,
            'cliente': reservacion.cliente.nombre,
            'nombre_evento': reservacion.nombreEvento,
            'descripcion': reservacion.descripEvento,
            'subtotal': str(reservacion.subtotal),
            'total': str(reservacion.total),
            'saldo_restante': str(saldo),
            'pagos_count': pagos_count,
            'estado': reservacion.estado_reserva.nombre
        })

class ListarReservacionesView(APIView):
    def get(self, request):
        reservaciones = models.Reservacion.objects.all()
        data = serializers.ReservacionSerializers(reservaciones, many = True).data
        return Response(data)

class LlenarCalendarioReservaciones(APIView):
    def get(self, request):
        from datetime import datetime, date
        # Excluir solicitudes (SOLIC y PEN)
        reservaciones = models.Reservacion.objects.exclude(
            estado_reserva__codigo__in=['SOLIC', 'PEN']
        ).exclude(
            es_paquete=True
        ).exclude(
            fechaEvento__isnull=True
        )
        
        eventos = []
        for reservacion in reservaciones:
            start = datetime.combine(reservacion.fechaEvento, reservacion.horaInicio)
            end = datetime.combine(reservacion.fechaEvento, reservacion.horaFin)
            eventos.append({
                'title': reservacion.nombreEvento,
                'start': start.isoformat(),
                'end': end.isoformat(),
            })
        
        return Response(eventos)

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
            
            decoded = auth.verify_id_token(token, clock_skew_seconds=10)
            firebase_uid = decoded['uid']
            email = decoded.get('email', '')

            try:
                cuenta = models.Cuenta.objects.get(firebase_uid=firebase_uid)
            except models.Cuenta.DoesNotExist:
                return JsonResponse({'error': 'Cuenta no registrada en el sistema'}, status=404)

            request.session['cuenta_id'] = cuenta.id
            request.session['firebase_uid'] = firebase_uid
            request.session.modified = True

            # Obtener el rol del usuario
            rol_codigo = None
            try:
                trabajador = models.Trabajador.objects.get(cuenta=cuenta)
                rol_codigo = trabajador.rol.codigo
            except models.Trabajador.DoesNotExist:
                # No es trabajador, es cliente
                rol_codigo = 'CLIENTE'

            return JsonResponse({'success': True, 'user': {
                'id': cuenta.id,
                'nombre': cuenta.nombre_usuario,
                'email': cuenta.correo_electronico,
                'rol': rol_codigo
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
                'cuenta_id': cuenta.id,
                'tipo': 'cliente',
                'rol': None
            }
            
            try:
                trabajador = models.Trabajador.objects.select_related('rol').get(cuenta_id=cuenta.id)
                user_data['tipo'] = 'trabajador'
                user_data['rol'] = trabajador.rol.codigo
                user_data['nombre'] = trabajador.nombre
                user_data['no_empleado'] = trabajador.no_empleado
                user_data['rfc'] = trabajador.rfc
                user_data['telefono'] = trabajador.telefono
                user_data['apellidoPaterno'] = trabajador.apellidoPaterno
                user_data['apellidoMaterno'] = trabajador.apelidoMaterno
            except models.Trabajador.DoesNotExist:
                pass
            
            serializer = serializers.LoginResponseSerializer(user_data)
            return JsonResponse({'success': True, 'user': serializer.data})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


class PerfilView(APIView):
    """API para obtener el perfil del usuario logueado (trabajador o cliente)"""
    def get(self, request):
        email = request.query_params.get('email')
        
        if not email:
            return Response({'error': 'email requerido'}, status=400)
        
        try:
            cuenta = models.Cuenta.objects.get(correo_electronico=email)
            
            # Verificar si es trabajador
            try:
                trabajador = models.Trabajador.objects.select_related(
                    'cuenta', 'rol'
                ).get(cuenta=cuenta)
                
                serializer = serializers.PerfilSerializer(trabajador)
                data = serializer.data
                data['tipo_usuario'] = 'trabajador'
                return Response(data)
            except models.Trabajador.DoesNotExist:
                pass
            
            # Si no es trabajador, verificar si es cliente
            try:
                datos_cliente = models.DatosCliente.objects.get(cuenta=cuenta)
                
                serializer = serializers.DatosClienteSerializer(datos_cliente)
                data = serializer.data
                data['tipo_usuario'] = 'cliente'
                data['nombre_usuario'] = cuenta.nombre_usuario
                return Response(data)
            except models.DatosCliente.DoesNotExist:
                pass
            
            # Si neither worker nor client, return basic cuenta data
            return Response({
                'tipo_usuario': 'cliente_sin_datos',
                'correo_electronico': cuenta.correo_electronico,
                'nombre_usuario': cuenta.nombre_usuario,
                'nombre': '',
                'apellidoPaterno': '',
                'apellidoMaterno': '',
                'telefono': '',
                'rfc': '',
                'nombre_fiscal': '',
            })
            
        except models.Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=404)

    # === DATOS DEL CLIENTE ===
    # POST: Crear/actualizar datos del cliente (para reservaciones)
    def post(self, request):
        import logging
        logger = logging.getLogger(__name__)
        
        email = request.data.get('correo_electronico')
        
        if not email:
            return Response({'error': 'correo_electronico requerido'}, status=400)
        
        try:
            cuenta = models.Cuenta.objects.get(correo_electronico=email)
            
            # Verificar si ya tiene datos de cliente
            datos_cliente = models.DatosCliente.objects.filter(cuenta=cuenta).first()
            
            if datos_cliente:
                # Actualizar
                datos_cliente.nombre = request.data.get('nombre', datos_cliente.nombre) or datos_cliente.nombre
                datos_cliente.apellidoPaterno = request.data.get('apellidoPaterno', datos_cliente.apellidoPaterno) or datos_cliente.apellidoPaterno
                datos_cliente.apelidoMaterno = request.data.get('apelidoMaterno') or datos_cliente.apelidoMaterno
                datos_cliente.rfc = request.data.get('rfc') or datos_cliente.rfc
                datos_cliente.nombre_fiscal = request.data.get('nombre_fiscal') or datos_cliente.nombre_fiscal
                datos_cliente.telefono = request.data.get('telefono') or datos_cliente.telefono
                datos_cliente.dir_colonia = request.data.get('dir_colonia') or datos_cliente.dir_colonia
                datos_cliente.dir_calle = request.data.get('dir_calle') or datos_cliente.dir_calle
                datos_cliente.dir_numero = request.data.get('dir_numero') or datos_cliente.dir_numero
                # datos_cliente.registrado_desde_app = True
                datos_cliente.save()
            else:
                # Crear nuevo
                tipo_cliente = models.TipoCliente.objects.first()
                if not tipo_cliente:
                    return Response({'error': 'No hay tipos de cliente configurados'}, status=400)
                
                datos_cliente = models.DatosCliente.objects.create(
                    rfc=request.data.get('rfc', '') or '',
                    nombre_fiscal=request.data.get('nombre_fiscal', '') or '',
                    nombre=request.data.get('nombre', '') or '',
                    apellidoPaterno=request.data.get('apellidoPaterno', '') or '',
                    telefono=request.data.get('telefono', '') or '',
                    correo_electronico=email,
                    dir_colonia=request.data.get('dir_colonia', '') or '',
                    dir_calle=request.data.get('dir_calle', '') or '',
                    dir_numero=request.data.get('dir_numero', '') or '',
                    tipo_cliente=tipo_cliente,
                    cuenta=cuenta,
                )
            
            serializer = serializers.DatosClienteSerializer(datos_cliente)
            return Response(serializer.data)
            
        except models.Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=404)
        except Exception as e:
            import traceback
            return Response({'error': f'Error interno: {str(e)}'}, status=500)

    # === ACTUALIZAR DATOS DE CUENTA (para perfil) ===
    # PUT: Actualizar nombre de usuario
    def put(self, request):
        import logging
        logger = logging.getLogger(__name__)
        
        email = request.data.get('correo_electronico')
        
        if not email:
            return Response({'error': 'correo_electronico requerido'}, status=400)
        
        try:
            cuenta = models.Cuenta.objects.get(correo_electronico=email)
            
            nuevo_nombre = request.data.get('nombre_usuario')
            if nuevo_nombre:
                cuenta.nombre_usuario = nuevo_nombre
                cuenta.save()
                logger.info(f"Cuenta updated: {cuenta.id}")
            
            serializer = serializers.CuentaSerializer(cuenta)
            return Response(serializer.data)
            
        except models.Cuenta.DoesNotExist:
            logger.error(f"Cuenta not found for email: {email}")
            return Response({'error': 'Cuenta no encontrada'}, status=404)
        except Exception as e:
            import traceback
            logger.error(f"Error in PerfilView PUT: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({'error': f'Error interno: {str(e)}'}, status=500)

    # === ACTUALIZAR IMAGEN DE PERFIL (comentado para revisión) ===
    # Descomentar después de agregar campo imagen_url en modelo
    # def post(self, request):
    #     email = request.data.get('email')
    #     imagen_url = request.data.get('imagen_url')
    #     
    #     if not email or not imagen_url:
    #         return Response({'error': 'email e imagen_url requeridos'}, status=400)
    #     
    #     try:
    #         cuenta = models.Cuenta.objects.get(correo_electronico=email)
    #         cuenta.imagen_url = imagen_url
    #         cuenta.save()
    #         return Response({'success': True, 'imagen_url': cuenta.imagen_url})
    #     except models.Cuenta.DoesNotExist:
    #         return Response({'error': 'Cuenta no encontrada'}, status=404)


@csrf_exempt
def api_signup(request):
    import logging
    logger = logging.getLogger(__name__)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Signup request data keys: {data.keys()}")

            token = data.get('token')
            nombre_usuario = data.get('nombre', '')

            if not token:
                logger.warning("Signup: Token requerido")
                return JsonResponse({'error': 'Token requerido'}, status=400)

            if not FIREBASE_ENABLED:
                logger.warning("Signup: Firebase no configurado")
                return JsonResponse({'error': 'Firebase no configurado'}, status=500)

            if len(token) > 10000:
                logger.warning("Signup: Token inválido (muy largo)")
                return JsonResponse({'error': 'Token inválido'}, status=400)

            decoded = auth.verify_id_token(token)
            firebase_uid = decoded['uid']
            email = decoded.get('email', '')
            display_name = decoded.get('name', '')
            logger.info(f"Signup: Firebase user verified - email: {email}")

            # Usar nombre de Flutter o el de Firebase
            nombre_final = nombre_usuario if nombre_usuario else display_name

            estado_cuenta = models.EstadoCuenta.objects.filter(codigo='ACT').first()

            # Verificar si la cuenta ya existe
            cuenta_existente = models.Cuenta.objects.filter(
                models.Q(firebase_uid=firebase_uid) | models.Q(correo_electronico=email)
            ).first()
            
            if cuenta_existente:
                logger.info(f"Signup: Cuenta existente para {email}")
                return JsonResponse({'success': True, 'message': 'Ya tenías una cuenta'})

            # Crear la cuenta
            cuenta = models.Cuenta.objects.create(
                nombre_usuario=nombre_final,
                correo_electronico=email,
                firebase_uid=firebase_uid,
                estado_cuenta=estado_cuenta,
            )
            
            logger.info(f"Signup: Cuenta creada para {email}")
            
            # Crear DatosCliente básico para que pueda hacer reservaciones
            # Se usa un tipo_cliente por defecto (el primero disponible)
            tipo_cliente_default = models.TipoCliente.objects.filter(disposicion=True).first()
            
            if tipo_cliente_default:
                models.DatosCliente.objects.create(
                    rfc='',  # Se actualizará después desde el perfil
                    nombre_fiscal='',
                    nombre=nombre_final,
                    apellidoPaterno='',
                    apelidoMaterno='',
                    telefono='',
                    correo_electronico=email,
                    dir_colonia='',
                    dir_calle='',
                    dir_numero='',
                    tipo_cliente=tipo_cliente_default,
                    cuenta=cuenta,
                )
                logger.info(f"Signup: DatosCliente creados para {email}")
            
            # Iniciar sesión automáticamente
            request.session['cuenta_id'] = cuenta.id
            request.session['firebase_uid'] = firebase_uid
            request.session.modified = True
            
            return JsonResponse({
                'success': True, 
                'message': 'Cuenta creada exitosamente',
                'cuenta_id': cuenta.id
            })

        except json.JSONDecodeError as e:
            logger.error(f"Signup: JSON decode error - {e}")
            return JsonResponse({'error': f'JSON inválido: {str(e)}'}, status=400)
        except Exception as e:
            logger.error(f"Signup: Error general - {type(e).__name__}: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


class DisponibilidadSalonesView(APIView):
    def get(self, request):
        from django.utils.dateparse import parse_date
        from datetime import date
        
        fecha_str = request.query_params.get('fecha')
        
        if not fecha_str:
            return Response({'error': 'Fecha no proporcionada'}, status=400)
        
        fecha = parse_date(fecha_str)
        if not fecha:
            return Response({'error': 'Formato de fecha inválido'}, status=400)
        
        # Obtener todos los salones
        salones = models.Salon.objects.all().select_related('estado_salon')
        
        # Obtener los IDs de salones ocupados/reservados en esa fecha
        salon_ids_ocupados = set(
            models.Reservacion.objects.filter(
                fechaEvento=fecha
            ).exclude(
                estado_reserva__codigo='CANCEL'
            ).values_list('montaje__salon_id', flat=True).distinct()
        )
        
        # Obtener estados de salon para esa fecha (desde RegistrEstadSalon)
        estados_fecha = {}
        registros = models.RegistrEstadSalon.objects.filter(
            fecha=fecha
        ).select_related('salon', 'estado_salon')
        
        for reg in registros:
            estados_fecha[reg.salon_id] = reg.estado_salon.codigo
        
        # Construir respuesta con disponibilidad
        resultado = []
        for salon in salones:
            # Primero verificar si hay reservacion
            esta_ocupado = salon.id in salon_ids_ocupados
            
            # Si no hay reservacion, verificar estado del salon en esa fecha
            estado_codigo = estados_fecha.get(salon.id)
            if estado_codigo:
                if estado_codigo in ('OCUP', 'RESV'):
                    esta_ocupado = True
                estado_nombre = {
                    'OCUP': 'Ocupado',
                    'RESV': 'Reservado',
                    'LIMPI': 'En Limpieza',
                    'MANTE': 'Mantenimiento',
                    'DISP': 'Disponible',
                }.get(estado_codigo, 'Disponible')
            else:
                estado_nombre = 'Ocupado' if esta_ocupado else 'Disponible'
            
            resultado.append({
                'id': salon.id,
                'nombre': salon.nombre,
                'capacidad': salon.maxCapacidad if salon.maxCapacidad else 0,
                'precio': float(salon.costo) if salon.costo else 0,
                'estado': estado_nombre,
                'reservado': esta_ocupado,
            })
        
        return Response(resultado)
        # === CÓDIGO COMENTADO - Available for reference ===
        # Original: devolvía salones con su estado (no reservaciones)
        # salones = models.Salon.objects.select_related('estado_salon').all()
        #
        # def get_estado_actual(salon):
        #     """Retorna el estado actual considerando fecha_fin"""
        #     ultimo = models.RegistrEstadSalon.objects.filter(salon=salon).order_by('-fecha').first()
        #     if ultimo and hasattr(ultimo, 'fecha_fin') and ultimo.fecha_fin and ultimo.fecha_fin < date.today():
        #         return models.EstadoSalon.objects.get(codigo='DISP')
        #     return ultimo.estado_salon if ultimo else salon.estado_salon
        #
        # # Filtrar salones que NO estén en estados no reservables
        # estados_no_reservables = ['LIM', 'MANT', 'NODISP']  # códigos que bloquean reserva
        # salones = [s for s in salones if get_estado_actual(s).codigo not in estados_no_reservables]
        #
        # serializer = serializers.SalonEstadoSerializer(salones, many=True)
        # return Response(serializer.data)


class ReservacionesPorFechaView(APIView):
    def get(self, request):
        from django.utils.dateparse import parse_date
        
        fecha_str = request.query_params.get('fecha')
        
        if not fecha_str:
            return Response({'error': 'Fecha no proporcionada'}, status=400)
        
        fecha = parse_date(fecha_str)
        if not fecha:
            return Response({'error': 'Formato de fecha inválido'}, status=400)
        
        reservaciones = models.Reservacion.objects.filter(
            fechaEvento=fecha
        ).select_related(
            'cliente', 'montaje__salon', 'estado_reserva'
        )
        
        serializer = serializers.ReservacionResumenSerializer(reservaciones, many=True)
        return Response({'reservaciones': serializer.data})


class DetalleReservacionView(APIView):
    """API para obtener detalles completos de una reservación"""
    def get(self, request, pk):
        try:
            reservacion = models.Reservacion.objects.select_related(
                'cliente__cuenta', 'cliente__tipo_cliente',
                'montaje__salon', 'montaje__tipo_montaje',
                'estado_reserva', 'tipo_evento'
            ).prefetch_related(
                'reservaservicio_set__servicio', 
                'reservaequipa_set__equipamiento',
                'montaje__montajemobiliario_set__mobiliario'
            ).get(pk=pk)
            
            serializer = serializers.ReservacionCoordinadorSerializer(reservacion)
            return Response(serializer.data)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)


class ChecklistAlmacenistaView(APIView):
    """API para obtener el checklist del almacenista"""
    def get(self, request, pk):
        try:
            reservacion = models.Reservacion.objects.get(pk=pk)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)
        
        return Response({
            'checklist_almacenista': reservacion.checklist_almacenista or {}
        })


class ChecklistCoordinadorView(APIView):
    """API para obtener el checklist del coordinador"""
    def get(self, request, pk):
        try:
            reservacion = models.Reservacion.objects.get(pk=pk)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)
        
        return Response({
            'checklist_coordinador': reservacion.checklist_coordinador or {},
            'progreso_checklist': reservacion.progreso_checklist or 0.0
        })


class ChecklistUpdateView(APIView):
    """API para actualizar el checklist de una reservación"""
    def post(self, request, pk):
        try:
            reservacion = models.Reservacion.objects.get(pk=pk)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)
        
        tipo = request.data.get('tipo')  # 'coordinador' o 'almacenista'
        checklist = request.data.get('checklist', {})
        
        if not tipo or tipo not in ['coordinador', 'almacenista']:
            return Response({'error': 'Tipo de checklist inválido'}, status=400)
        
        # Actualizar el checklist correspondiente
        if tipo == 'coordinador':
            # Mantener todos los 14 items del checklist
            current_checklist = dict(reservacion.checklist_coordinador) if reservacion.checklist_coordinador else {}
            print(f"DEBUG Backend: current_checklist antes = {current_checklist}")
            print(f"DEBUG Backend: checklist recibido = {checklist}")
            current_checklist.update(checklist)
            print(f"DEBUG Backend: current_checklist después = {current_checklist}")
            reservacion.checklist_coordinador = current_checklist
            
            # Calcular progreso: solo contar valores booleanos (excluir el item_9 que es automático)
            boolean_values = [v for k, v in current_checklist.items() if isinstance(v, bool)]
            if boolean_values:
                completed = sum(1 for v in boolean_values if v == True)
                total = len(boolean_values)
                reservacion.progreso_checklist = completed / total if total > 0 else 0
        else:
            # Mantener el checklist existente y actualizar
            current_checklist = dict(reservacion.checklist_almacenista) if reservacion.checklist_almacenista else {}
            print(f"DEBUG Backend: checklist_almacenista actual = {current_checklist}")
            print(f"DEBUG Backend: checklist recibido almacenista = {checklist}")
            current_checklist.update(checklist)
            print(f"DEBUG Backend: checklist_almacenista nuevo = {current_checklist}")
            reservacion.checklist_almacenista = current_checklist
            
            # Si es almacenista, también marcar automáticamente el item #9 del coordinador
            coord_checklist = dict(reservacion.checklist_coordinador) if reservacion.checklist_coordinador else {}
            coord_checklist['item_9'] = True
            reservacion.checklist_coordinador = coord_checklist
            
            # Recalcular progreso del coordinador (solo booleanos)
            boolean_values = [v for k, v in coord_checklist.items() if isinstance(v, bool)]
            if boolean_values:
                completed = sum(1 for v in boolean_values if v == True)
                total = len(boolean_values)
                reservacion.progreso_checklist = completed / total if total > 0 else 0
        
        reservacion.save()
        
        return Response({
            'success': True,
            'checklist_coordinador': reservacion.checklist_coordinador,
            'checklist_almacenista': reservacion.checklist_almacenista,
            'progreso_checklist': reservacion.progreso_checklist
        })


class ReservacionProgresoView(APIView):
    """API para obtener el progreso del checklist de una reservación"""
    def get(self, request, pk):
        try:
            reservacion = models.Reservacion.objects.select_related(
                'estado_reserva'
            ).get(pk=pk)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)
        
        serializer = serializers.ReservacionProgresoSerializer(reservacion)
        return Response(serializer.data)


class ReservacionFormularioView(APIView):
    """API para obtener datos de una reservación en formato de formulario"""
    def get(self, request, pk):
        try:
            reservacion = models.Reservacion.objects.select_related(
                'cliente', 'cliente__cuenta', 'montaje__salon', 'montaje__tipo_montaje',
                'tipo_evento'
            ).prefetch_related(
                'reservaservicio_set__servicio', 'reservaequipa_set__equipamiento', 'montaje__montajemobiliario_set__mobiliario'
            ).get(pk=pk)
            
            serializer = serializers.ReservacionFormularioSerializer(reservacion)
            return Response(serializer.data)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class CambiarEstadoReservacionView(APIView):
    """API para cambiar el estado de una reservación"""
    def post(self, request, pk):
        try:
            nuevo_estado = request.data.get('estado')
            if not nuevo_estado:
                return Response({'error': 'Estado no proporcionado'}, status=400)
            
            reservacion = models.Reservacion.objects.get(pk=pk)
            estado = models.EstadoReserva.objects.get(codigo=nuevo_estado)
            
            reservacion.estado_reserva = estado
            reservacion.save()
            
            models.RegistrEstadReserva.objects.create(
                reservacion_id=reservacion.pk,
                estado_reserva=estado
            )
            
            return Response({'mensaje': 'Estado actualizado correctamente', 'estado': estado.nombre})
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)
        except models.EstadoReserva.DoesNotExist:
            return Response({'error': 'Estado no válido'}, status=400)


class ListaReservacionesCoordinadorView(APIView):
    """API para listar todas las reservaciones del coordinador"""
    def get(self, request):
        reservaciones = models.Reservacion.objects.select_related(
            'cliente__cuenta', 'montaje__salon', 'montaje__tipo_montaje',
            'estado_reserva'
        ).prefetch_related(
            'reservaservicio_set', 'reservaequipa_set__equipamiento'
        ).order_by('-fechaEvento')
        
        serializer = serializers.ReservacionCoordinadorSerializer(reservaciones, many=True)
        return Response(serializer.data)


class MisReservacionesView(APIView):
    """API para listar las reservaciones del cliente logueado"""
    def get(self, request):
        email = request.query_params.get('email')
        
        if not email:
            return Response({'error': 'Email requerido'}, status=400)
        
        try:
            cuenta = models.Cuenta.objects.get(correo_electronico=email)
            datos_cliente = models.DatosCliente.objects.get(cuenta=cuenta)
        except models.Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=404)
        except models.DatosCliente.DoesNotExist:
            return Response({'reservaciones': []})
        
        reservaciones = models.Reservacion.objects.filter(
            cliente=datos_cliente
        ).select_related(
            'cliente', 'montaje__salon', 'montaje__tipo_montaje',
            'estado_reserva', 'tipo_evento'
        ).order_by('-fechaEvento')
        
        resultado = []
        for r in reservaciones:
            resultado.append({
                'id': r.id,
                'nombre': r.nombreEvento,
                'descripcion': r.descripEvento,
                'fecha': r.fechaEvento.isoformat() if r.fechaEvento else None,
                'hora_inicio': r.horaInicio.isoformat() if r.horaInicio else None,
                'hora_fin': r.horaFin.isoformat() if r.horaFin else None,
                'asistentes': r.estimaAsistentes,
                'estado_codigo': r.estado_reserva.codigo,
                'estado_nombre': r.estado_reserva.nombre,
                'salon_nombre': r.montaje.salon.nombre if r.montaje else None,
                'montaje_nombre': r.montaje.tipo_montaje.nombre if r.montaje and r.montaje.tipo_montaje else None,
                'total': float(r.total) if r.total else 0,
            })
        
        return Response({'reservaciones': resultado})


class ReservacionProximaView(APIView):
    """API para obtener la reservación más próxima del cliente"""
    def get(self, request):
        email = request.query_params.get('email')
        
        if not email:
            return Response({'error': 'Email requerido'}, status=400)
        
        try:
            cuenta = models.Cuenta.objects.get(correo_electronico=email)
            datos_cliente = models.DatosCliente.objects.get(cuenta=cuenta)
        except models.Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=404)
        except models.DatosCliente.DoesNotExist:
            return Response({'reservacion': None})
        
        from django.utils import timezone
        from datetime import date
        
        reservacion = models.Reservacion.objects.filter(
            cliente=datos_cliente,
            fechaEvento__gte=date.today()
        ).select_related(
            'cliente__cuenta', 'cliente__tipo_cliente',
            'montaje__salon', 'montaje__tipo_montaje',
            'estado_reserva', 'tipo_evento'
        ).prefetch_related(
            'reservaservicio_set__servicio', 
            'reservaequipa_set__equipamiento',
            'montaje__montajemobiliario_set__mobiliario'
        ).order_by('fechaEvento').first()
        
        if not reservacion:
            return Response({'reservacion': None})
        
        serializer = serializers.ReservacionCoordinadorSerializer(reservacion)
        return Response({'reservacion': serializer.data})


class ListaPaquetesView(APIView):
    """API para listar paquetes disponibles (para móvil)"""
    def get(self, request):
        paquetes = models.Reservacion.objects.filter(
            es_paquete=True
        ).select_related(
            'montaje__salon', 'montaje__tipo_montaje'
        ).prefetch_related(
            'reservaservicio_set__servicio',
            'reservaequipa_set__equipamiento'
        ).order_by('nombre_paquete')
        
        serializer = serializers.PaqueteSerializer(paquetes, many=True)
        return Response(serializer.data)


class DetallePaqueteView(APIView):
    """API para obtener detalle de un paquete (para móvil)"""
    def get(self, request, pk):
        try:
            paquete = models.Reservacion.objects.select_related(
                'montaje__salon', 'montaje__tipo_montaje'
            ).prefetch_related(
                'reservaservicio_set__servicio',
                'reservaequipa_set__equipamiento'
            ).get(pk=pk, es_paquete=True)
            
            serializer = serializers.PaqueteSerializer(paquete)
            return Response(serializer.data)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Paquete no encontrado'}, status=404)


class ReservacionesFechaView(APIView):
    """API para obtener las reservaciones de una fecha específica"""
    def get(self, request):
        from django.utils.dateparse import parse_date
        
        fecha_str = request.query_params.get('fecha')
        
        if not fecha_str:
            return Response({'error': 'Fecha no proporcionada'}, status=400)
        
        fecha = parse_date(fecha_str)
        if not fecha:
            return Response({'error': 'Formato de fecha inválido'}, status=400)
        
        reservaciones = models.Reservacion.objects.filter(
            fechaEvento=fecha
        ).exclude(
            estado_reserva__codigo='CANCEL'
        ).select_related(
            'montaje__salon', 'tipo_evento', 'cliente__cuenta'
        )
        
        resultado = []
        for r in reservaciones:
            resultado.append({
                'id': r.id,
                'salon_nombre': r.montaje.salon.nombre if r.montaje and r.montaje.salon else None,
                'salon_id': r.montaje.salon.id if r.montaje and r.montaje.salon else None,
                'fechaEvento': r.fechaEvento.isoformat() if r.fechaEvento else None,
                'horaInicio': r.horaInicio.isoformat() if r.horaInicio else None,
                'horaFin': r.horaFin.isoformat() if r.horaFin else None,
                'nombreEvento': r.nombreEvento,
                'tipo_evento_nombre': r.tipo_evento.nombre if r.tipo_evento else None,
                'cliente_nombre': r.cliente.cuenta.nombre_usuario if r.cliente and r.cliente.cuenta else None,
            })
        
        return Response(resultado)


class SolicitudesExtraView(APIView):
    """API para obtener las solicitudes extra (mobiliario, equipamiento y servicios) de reservaciones activas"""
    # Estados activos: SOLIC (solicitud), PEN (pendiente), CONF/CON (confirmada), PROC (en proceso)
    estados_activos = ['SOLIC', 'PEN', 'CONF', 'CON', 'PROC']
    
    def get(self, request):
        reservaciones = models.Reservacion.objects.filter(
            estado_reserva__codigo__in=self.estados_activos
        ).select_related(
            'montaje__salon', 'cliente__cuenta', 'estado_reserva'
        ).prefetch_related(
            'montaje__montajemobiliario_set__mobiliario',
            'reservaequipa_set__equipamiento',
            'reservaservicio_set__servicio'
        )
        
        resultado = []
        for r in reservaciones:
            mobiliarios_extra = []
            equipamentos_extra = []
            servicios_extra = []
            
            if r.montaje:
                for mm in r.montaje.montajemobiliario_set.all():
                    if mm.extra:
                        mobiliarios_extra.append({
                            'id': mm.id,
                            'mobiliario_id': mm.mobiliario.id,
                            'nombre': mm.mobiliario.nombre,
                            'descripcion': mm.mobiliario.descripcion,
                            'cantidad': mm.cantidad,
                            'precio': float(mm.mobiliario.costo) if mm.mobiliario.costo else 0,
                            'completado': mm.completado or False,
                        })
            
            for re in r.reservaequipa_set.all():
                if re.extra:
                    equipamentos_extra.append({
                        'id': re.id,
                        'equipamiento_id': re.equipamiento.id,
                        'nombre': re.equipamiento.nombre,
                        'descripcion': re.equipamiento.descripcion,
                        'cantidad': re.cantidad,
                        'precio': float(re.equipamiento.costo) if re.equipamiento.costo else 0,
                        'completado': re.completado or False,
                    })
            
            for rs in r.reservaservicio_set.all():
                if rs.extra:
                    servicios_extra.append({
                        'id': rs.id,
                        'servicio_id': rs.servicio.id,
                        'nombre': rs.servicio.nombre,
                        'descripcion': rs.servicio.descripcion,
                        'precio': float(rs.servicio.costo) if rs.servicio.costo else 0,
                        'completado': False,
                    })
            
            if mobiliarios_extra or equipamentos_extra or servicios_extra:
                resultado.append({
                    'id': r.id,
                    'nombre': r.nombreEvento,
                    'fecha': r.fechaEvento.isoformat() if r.fechaEvento else None,
                    'hora_inicio': r.horaInicio.isoformat() if r.horaInicio else None,
                    'hora_fin': r.horaFin.isoformat() if r.horaFin else None,
                    'salon_nombre': r.montaje.salon.nombre if r.montaje and r.montaje.salon else None,
                    'cliente_nombre': r.cliente.cuenta.nombre_usuario if r.cliente and r.cliente.cuenta else None,
                    'estado_codigo': r.estado_reserva.codigo,
                    'estado_nombre': r.estado_reserva.nombre,
                    'mobiliarios_extra': mobiliarios_extra,
                    'equipamiento_extra': equipamentos_extra,
                    'servicios_extra': servicios_extra,
                })
        
        return Response({'reservaciones': resultado})


class CompletarSolicitudExtraView(APIView):
    """API para marcar como completados los items extra de una reservación"""
    def patch(self, request, reservacion_id):
        try:
            reservacion = models.Reservacion.objects.get(pk=reservacion_id)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)
        
        mobiliarios = request.data.get('mobiliarios', [])
        equipamentos = request.data.get('equipamentos', [])
        
        errores = []
        
        for mob_data in mobiliarios:
            try:
                mm = models.MontajeMobiliario.objects.get(
                    pk=mob_data.get('id'),
                    montaje__reservacion=reservacion
                )
                mm.completado = mob_data.get('completado', False)
                mm.save(update_fields=['completado'])
            except models.MontajeMobiliario.DoesNotExist:
                errores.append(f"Mobiliario {mob_data.get('id')} no encontrado")
        
        for eq_data in equipamentos:
            try:
                re = models.ReservaEquipa.objects.get(
                    pk=eq_data.get('id'),
                    reservacion=reservacion
                )
                re.completado = eq_data.get('completado', False)
                re.save(update_fields=['completado'])
            except models.ReservaEquipa.DoesNotExist:
                errores.append(f"Equipamiento {eq_data.get('id')} no encontrado")
        
        if errores:
            return Response({'error': 'Algunos items no se actualizaron', 'detalles': errores}, status=400)
        
        return Response({'mensaje': 'Items actualizados correctamente'})


class MisSolicitudesExtraView(APIView):
    """API para obtener las solicitudes extra de las reservaciones del cliente"""
    def get(self, request):
        import logging
        logger = logging.getLogger(__name__)
        
        email = request.query_params.get('email')
        
        if not email:
            return Response({'error': 'Email requerido'}, status=400)
        
        try:
            cuenta = models.Cuenta.objects.get(correo_electronico=email)
            datos_cliente = models.DatosCliente.objects.get(cuenta=cuenta)
            logger.info(f"Cliente encontrado: {datos_cliente.id}, cuenta: {cuenta.id}")
        except models.Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=404)
        except models.DatosCliente.DoesNotExist:
            return Response({'solicitudes': []})
        
        # Obtener reservaciones del cliente
        reservaciones = models.Reservacion.objects.filter(
            cliente=datos_cliente,
            estado_reserva__codigo__in=['SOLIC', 'PEN', 'CONF', 'CON', 'PROC']
        ).select_related(
            'montaje__salon', 'estado_reserva'
        ).prefetch_related(
            'montaje__montajemobiliario_set__mobiliario',
            'reservaequipa_set__equipamiento',
            'reservaservicio_set__servicio'
        )
        
        logger.info(f"Reservaciones encontradas para cliente {datos_cliente.id}: {reservaciones.count()}")
        
        resultado = []
        for r in reservaciones:
            logger.info(f"Reservacion {r.id}: montaje={r.montaje}, cliente={r.cliente}")
            
            mobiliarios_extra = []
            equipamentos_extra = []
            servicios_extra = []
            
            if r.montaje:
                logger.info(f"  Montaje {r.montaje.id}: mobiliarios={r.montaje.montajemobiliario_set.count()}")
                for mm in r.montaje.montajemobiliario_set.all():
                    logger.info(f"    Mobiliario {mm.id}: extra={mm.extra}, mobiliario={mm.mobiliario.id}")
                    if mm.extra:
                        mobiliarios_extra.append({
                            'id': mm.id,
                            'mobiliario_id': mm.mobiliario.id,
                            'nombre': mm.mobiliario.nombre,
                            'cantidad': mm.cantidad,
                            'precio_unitario': float(mm.mobiliario.costo) if mm.mobiliario.costo else 0,
                            'costo_total': float(mm.mobiliario.costo * mm.cantidad) if mm.mobiliario.costo else 0,
                        })
            
            for re in r.reservaequipa_set.all():
                if re.extra:
                    equipamentos_extra.append({
                        'id': re.id,
                        'equipamiento_id': re.equipamiento.id,
                        'nombre': re.equipamiento.nombre,
                        'cantidad': re.cantidad,
                        'precio_unitario': float(re.equipamiento.costo) if re.equipamiento.costo else 0,
                        'costo_total': float(re.equipamiento.costo * re.cantidad) if re.equipamiento.costo else 0,
                    })
            
            for rs in r.reservaservicio_set.all():
                if rs.extra:
                    servicios_extra.append({
                        'id': rs.id,
                        'servicio_id': rs.servicio.id,
                        'nombre': rs.servicio.nombre,
                        'precio': float(rs.servicio.costo) if rs.servicio.costo else 0,
                    })
            
            # Solo incluir si hay extras
            if mobiliarios_extra or equipamentos_extra or servicios_extra:
                resultado.append({
                    'reservacion_id': r.id,
                    'reservacion_nombre': r.nombreEvento,
                    'reservacion_fecha': r.fechaEvento.isoformat() if r.fechaEvento else None,
                    'salon_nombre': r.montaje.salon.nombre if r.montaje and r.montaje.salon else None,
                    'estado_codigo': r.estado_reserva.codigo,
                    'mobiliarios_extra': mobiliarios_extra,
                    'equipamiento_extra': equipamentos_extra,
                    'servicios_extra': servicios_extra,
                })
        
        return Response({'solicitudes': resultado})
