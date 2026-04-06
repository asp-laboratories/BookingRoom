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
    queryset = models.Mobiliario.objects.prefetch_related('caracter_mobi').all()
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
        if self.action in ['list', 'retrieve']:
            return serializers.SalonEstadoSerializer
        return serializers.SalonSerializer

    def update(self, request, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        
        salon = self.get_object()
        nuevo_estado_input = request.data.get('estado_salon')
        
        if nuevo_estado_input:
            # Mapeo de códigos Flutter a códigos DB
            codigo_map = {
                'DISP': 'DIS',
                'LIM': 'LIM',
                'NODISP': 'NODIS',
                'RESV': 'RESV',
                'LIMPIEZA': 'LIM',
                'DISPONIBLE': 'DIS',
                'NO_DISPONIBLE': 'NODIS',
                'RESERVADO': 'RESV',
            }
            
            codigo_buscar = codigo_map.get(nuevo_estado_input.upper(), nuevo_estado_input.upper())
            
            try:
                nuevo_estado = models.EstadoSalon.objects.get(codigo=codigo_buscar)
                
                salon.estado_salon = nuevo_estado
                salon.save()
                
                models.RegistrEstadSalon.objects.create(
                    salon=salon,
                    estado_salon=nuevo_estado
                )
                
                serializer = serializers.SalonEstadoSerializer(salon)
                return Response(serializer.data)
                    
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
                    serializer = serializers.SalonEstadoSerializer(salon)
                    return Response(serializer.data)
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
        
        if self.action in ['list', 'retrieve']:
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
            new_reservacion = reservacionesService.crear_reseracion(validador.validated_data)
            respeusta = serializers.ReservacionLecturaSerializer(new_reservacion)
            return Response(respeusta.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)




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
        reservaciones = models.Reservacion.objects.all()
        
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
            
            cuenta, created = models.Cuenta.objects.get_or_create(
                firebase_uid=firebase_uid,
                defaults={
                    'nombre_usuario': nombre_final,
                    'correo_electronico': email,
                    'estado_cuenta': estado_cuenta,
                }
            )
            
            if created:
                logger.info(f"Signup: Cuenta creada para {email}")
                return JsonResponse({'success': True, 'message': 'Cuenta creada exitosamente'})
            else:
                logger.info(f"Signup: Cuenta existente para {email}")
                return JsonResponse({'success': True, 'message': 'Ya tenías una cuenta'})
                
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
        
        # Reservaciones de la fecha
        reservaciones = models.Reservacion.objects.filter(
            fechaEvento=fecha
        ).select_related(
            'montaje__salon', 'tipo_evento'
        )
        
        serializer = serializers.DisponibilidadSalonSerializer(reservaciones, many=True)
        return Response(serializer.data)
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
                'reservaservicio_set', 'reservaequipa_set__equipamiento'
            ).get(pk=pk)
            
            serializer = serializers.ReservacionCoordinadorSerializer(reservacion)
            return Response(serializer.data)
        except models.Reservacion.DoesNotExist:
            return Response({'error': 'Reservación no encontrada'}, status=404)


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
