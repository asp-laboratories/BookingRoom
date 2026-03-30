from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import transaction
from . import models

try:
    import firebase_admin
    from firebase_admin import auth

    FIREBASE_ENABLED = True
except:
    FIREBASE_ENABLED = False


def get_user_rol(request):
    cuenta_id = request.session.get("cuenta_id")
    if not cuenta_id:
        return None
    try:
        trabajador = models.Trabajador.objects.select_related("rol").get(
            cuenta_id=cuenta_id
        )
        return trabajador.rol.codigo
    except:
        return None


def get_cuenta_and_rol(request):
    cuenta_id = request.session.get("cuenta_id")
    if not cuenta_id:
        return None, None
    try:
        cuenta = models.Cuenta.objects.get(id=cuenta_id)
        try:
            trabajador = models.Trabajador.objects.select_related("rol").get(
                cuenta_id=cuenta_id
            )
            rol = trabajador.rol.codigo
        except models.Trabajador.DoesNotExist:
            rol = None
        return cuenta, rol
    except:
        return None, None


def require_login(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("cuenta_id"):
            return HttpResponseRedirect(reverse("login"))
        return view_func(request, *args, **kwargs)

    return wrapper


def login(request):
    return render(request, "BookingRoomApp/auth/login.html")


def sign_up(request):
    return render(request, "BookingRoomApp/auth/sign_up.html")


def home(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    return render(
        request, "BookingRoomApp/recepcion/home.html", {"cuenta": cuenta, "rol": rol}
    )


class Home(generic.View):
    template_name = "BookingRoomApp/recepcion/home.html"
    context = {}

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        reservaciones = models.Reservacion.objects.all()[:10]

        context = {
            "cuenta": cuenta,
            "rol": rol,
            "reservaciones": reservaciones,
        }
        return render(request, self.template_name, context)


class HistorialReservacionViw(generic.View):
    template_name = "BookingRoomApp/recepcion/historial_reservacion.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        reservaciones = models.Reservacion.objects.select_related(
            "cliente",
            "estado_reserva",
            "montaje__salon",
        )
        estados = models.EstadoReserva.objects.all()
        reservacion_total = models.Reservacion.objects.count()

        nombre = request.GET.get('nombre', '')
        estado_filtro = request.GET.get('estado', '')
        
        if nombre:
            reservaciones = reservaciones.filter(
                Q(nombreEvento__icontains=nombre) |
                Q(cliente__nombre__icontains=nombre)
            )
        
        if estado_filtro:
            reservaciones = reservaciones.filter(estado_reserva__codigo=estado_filtro)

        reservaciones = reservaciones.order_by('-id').all()

        return render(request, self.template_name, {
            "reservaciones": reservaciones,
            "estados": estados,
            "rol": rol,
            "nombre": nombre,
            "estado_filtro": estado_filtro,
            "reservacion_total": reservacion_total
        })


class ReservacionView(generic.View):
    template_name = "BookingRoomApp/recepcion/reservacion.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        context = {
            "tipos_servicio": models.TipoServicio.objects.filter(disposicion=True),
            "tipos_equipa": models.TipoEquipa.objects.filter(disposicion=True),
            "rol": rol,
        }
        return render(request, self.template_name, context)


class DetallesReservacionView(generic.DetailView):
    template_name = "BookingRoomApp/home/"
    model = models.Reservacion
    context_object_name = "reservacion"


def reservacion_detalle_json(request, pk):
    reserva = get_object_or_404(
        models.Reservacion.objects.select_related(
            "cliente",
            "montaje__salon",
            "montaje__tipo_montaje",
            "estado_reserva",
            "tipo_evento",
        ),
        pk=pk,
    )

    servicios = list(reserva.reserva_servicio.values_list("nombre", flat=True))

    data = {
        "id": reserva.pk,
        "nombre_evento": reserva.nombreEvento,
        "descripcion": reserva.descripEvento,
        "fecha": reserva.fechaEvento.isoformat(),
        "hora_inicio": reserva.horaInicio.strftime("%H:%M"),
        "hora_fin": reserva.horaFin.strftime("%H:%M"),
        "estado": reserva.estado_reserva.nombre,
        "asistentes": reserva.estimaAsistentes,
        "salon": reserva.montaje.salon.nombre
        if reserva.montaje and reserva.montaje.salon
        else "N/A",
        "montaje": reserva.montaje.tipo_montaje.nombre
        if reserva.montaje and reserva.montaje.tipo_montaje
        else "N/A",
        "tipo_evento": reserva.tipo_evento.nombre if reserva.tipo_evento else "N/A",
        "subtotal": str(reserva.subtotal),
        "iva": str(reserva.IVA),
        "total": str(reserva.total),
        "cliente": {
            "nombre": reserva.cliente.nombre,
            "apellido_paterno": reserva.cliente.apellidoPaterno,
            "apellido_materno": reserva.cliente.apelidoMaterno or "",
            "correo": reserva.cliente.correo_electronico,
            "telefono": reserva.cliente.telefono,
            "rfc": reserva.cliente.rfc,
            "nombre_fiscal": reserva.cliente.nombre_fiscal,
        },
        "servicios": servicios,
    }
    return JsonResponse(data)


def historial_detalle(request, pk):
    reservacion = get_object_or_404(models.Reservacion, pk=pk)

    pagos = models.Pago.objects.filter(reservacion=reservacion).order_by("no_pago")

    primer_pago = 0
    segundo_pago = 0

    for pago in pagos:
        if pago.no_pago == 1:
            primer_pago = pago.monto
        elif pago.no_pago == 2:
            segundo_pago = pago.monto

    ultimo_pago = pagos.order_by("-no_pago").first()
    saldo = ultimo_pago.saldo if ultimo_pago else reservacion.total

    data = {
        "total": str(reservacion.total),
        "subtotal": str(reservacion.subtotal),
        "iva": str(reservacion.IVA),
        "primer_pago": str(primer_pago),
        "segundo_pago": str(segundo_pago),
        "saldo": str(saldo),
    }

    return JsonResponse(data)


# def servicios(request):
#     cuenta, rol = get_cuenta_and_rol(request)
#     if not cuenta:
#         return HttpResponseRedirect(reverse("login"))

#     return render(request, "BookingRoomApp/administracion/servicios.html", {"rol": rol})


class Servicios(generic.ListView):
    template_name = "BookingRoomApp/administracion/servicios.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        servicios = models.Servicio.objects.select_related("tipo_servicio")
        servicio_total = models.Servicio.objects.count()
        tipo_servicio = models.TipoServicio.objects.filter(disposicion=True)
        
        nombre = request.GET.get('nombre', '')
        tipo = request.GET.get('tipo', '')
        orden = request.GET.get('orden', '')
        disposicion = request.GET.get('disposicion', '')
        
        if nombre:
            servicios = servicios.filter(nombre__icontains=nombre)
        
        if tipo:
            servicios = servicios.filter(tipo_servicio_id=tipo)
        
        if orden == 'costo_asc':
            servicios = servicios.order_by('costo')
        elif orden == 'costo_desc':
            servicios = servicios.order_by('-costo')
        else:
            servicios = servicios.order_by('-id')
        
        if disposicion == 'true':
            servicios = servicios.filter(disposicion=True)
        elif disposicion == 'false':
            servicios = servicios.filter(disposicion=False)
        
        servicios = servicios.all()

        return render(
            request,
            self.template_name,
            {
                "servicios": servicios,
                "tipo_servicio": tipo_servicio,
                "rol": rol,
                "nombre": nombre,
                "orden": orden,
                "disposicion": disposicion,
                "servicio_total": servicio_total,
            },
        )

    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        form_servicios = request.POST.get("form_servicios")

        if form_servicios == "servicio":
            nombre = request.POST.get("nameServicio")
            descripcion = request.POST.get("descripcion")
            costo = request.POST.get("costoServicio")
            tipo_servicio_id = request.POST.get("tipo_servicio")

            tipo_servicio = models.TipoServicio.objects.get(pk=tipo_servicio_id)

            models.Servicio.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                costo=costo,
                disposicion=True,
                tipo_servicio=tipo_servicio,
            )

            messages.success(request, f'El servicio: {nombre} fue registrado exitosamente')

        return HttpResponseRedirect(reverse("servicios"))


@csrf_exempt
def actualizar_servicio(request, pk):
    if request.method == 'POST':
        try:
            servicio = models.Servicio.objects.get(pk=pk)
            
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            costo = request.POST.get('costo')
            tipo_servicio_id = request.POST.get('tipo_servicio')
            disposicion = request.POST.get('disposicion') == 'true'
            
            if nombre:
                servicio.nombre = nombre
            if descripcion:
                servicio.descripcion = descripcion
            if costo:
                servicio.costo = costo
            if tipo_servicio_id:
                tipo_servicio = models.TipoServicio.objects.get(pk=tipo_servicio_id)
                servicio.tipo_servicio = tipo_servicio
            
            servicio.disposicion = disposicion
            servicio.save()
            
            messages.success(request, f'Servicio "{servicio.nombre}" actualizado correctamente')
            return HttpResponseRedirect(reverse('servicios'))
            
        except models.Servicio.DoesNotExist:
            messages.error(request, 'Servicio no encontrado')
            return HttpResponseRedirect(reverse('servicios'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return HttpResponseRedirect(reverse('servicios'))
    
    return HttpResponseRedirect(reverse('servicios'))


def actualizar_salon(request, pk):
    if request.method == 'POST':
        try:
            salon = models.Salon.objects.get(pk=pk)
            
            nombre = request.POST.get('nombre')
            costo = request.POST.get('costo')
            ubicacion = request.POST.get('ubicacion')
            dimenLargo = request.POST.get('dimenLargo')
            dimenAncho = request.POST.get('dimenAncho')
            dimenAlto = request.POST.get('dimenAlto')
            metrosCuadrados = request.POST.get('metrosCuadrados')
            maxCapacidad = request.POST.get('maxCapacidad')
            estado_salon_codigo = request.POST.get('estado_salon')
            
            if nombre:
                salon.nombre = nombre
            if costo:
                salon.costo = costo
            if ubicacion:
                salon.ubicacion = ubicacion
            if dimenLargo:
                salon.dimenLargo = dimenLargo
            if dimenAncho:
                salon.dimenAncho = dimenAncho
            if dimenAlto:
                salon.dimenAlto = dimenAlto
            if metrosCuadrados:
                salon.metrosCuadrados = metrosCuadrados
            if maxCapacidad:
                salon.maxCapacidad = maxCapacidad
            if estado_salon_codigo:
                estado = models.EstadoSalon.objects.get(codigo=estado_salon_codigo)
                salon.estado_salon = estado
            
            salon.save()
            
            messages.success(request, f'Salón "{salon.nombre}" actualizado correctamente')
            return HttpResponseRedirect(reverse('salones'))
            
        except models.Salon.DoesNotExist:
            messages.error(request, 'Salón no encontrado')
            return HttpResponseRedirect(reverse('salones'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return HttpResponseRedirect(reverse('salones'))
    
    return HttpResponseRedirect(reverse('salones'))


def actualizar_mobiliario(request, pk):
    if request.method == 'POST':
        try:
            mobiliario = models.Mobiliario.objects.get(pk=pk)
            
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            costo = request.POST.get('costo')
            stock = request.POST.get('stock')
            tipo_movil_id = request.POST.get('tipo_movil')
            
            if nombre:
                mobiliario.nombre = nombre
            if descripcion:
                mobiliario.descripcion = descripcion
            if costo:
                mobiliario.costo = costo
            if stock:
                mobiliario.stock = stock
            if tipo_movil_id:
                tipo_movil = models.TipoMobil.objects.get(pk=tipo_movil_id)
                mobiliario.tipo_movil = tipo_movil
            
            mobiliario.save()
            
            messages.success(request, f'Mobiliario "{mobiliario.nombre}" actualizado correctamente')
            return HttpResponseRedirect(reverse('mobiliario'))
            
        except models.Mobiliario.DoesNotExist:
            messages.error(request, 'Mobiliario no encontrado')
            return HttpResponseRedirect(reverse('mobiliario'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return HttpResponseRedirect(reverse('mobiliario'))
    
    return HttpResponseRedirect(reverse('mobiliario'))


def actualizar_equipamiento(request, pk):
    if request.method == 'POST':
        try:
            equipamiento = models.Equipamiento.objects.get(pk=pk)
            
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            costo = request.POST.get('costo')
            stock = request.POST.get('stock')
            tipo_equipa_id = request.POST.get('tipo_equipa')
            
            if nombre:
                equipamiento.nombre = nombre
            if descripcion:
                equipamiento.descripcion = descripcion
            if costo:
                equipamiento.costo = costo
            if stock:
                equipamiento.stock = stock
            if tipo_equipa_id:
                tipo_equipa = models.TipoEquipa.objects.get(pk=tipo_equipa_id)
                equipamiento.tipo_equipa = tipo_equipa
            
            equipamiento.save()
            
            messages.success(request, f'Equipamiento "{equipamiento.nombre}" actualizado correctamente')
            return HttpResponseRedirect(reverse('equipamiento'))
            
        except models.Equipamiento.DoesNotExist:
            messages.error(request, 'Equipamiento no encontrado')
            return HttpResponseRedirect(reverse('equipamiento'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return HttpResponseRedirect(reverse('equipamiento'))
    
    return HttpResponseRedirect(reverse('equipamiento'))


def actualizar_trabajador(request, pk):
    if request.method == 'POST':
        try:
            trabajador = models.Trabajador.objects.get(pk=pk)
            
            nombre = request.POST.get('nombre')
            apellidoPaterno = request.POST.get('apellidoPaterno')
            apellidoMaterno = request.POST.get('apellidoMaterno')
            telefono = request.POST.get('telefono')
            rfc = request.POST.get('rfc')
            rol_codigo = request.POST.get('rol')
            
            if nombre:
                trabajador.nombre = nombre
            if apellidoPaterno:
                trabajador.apellidoPaterno = apellidoPaterno
            if apellidoMaterno:
                trabajador.apelidoMaterno = apellidoMaterno
            if telefono:
                trabajador.telefono = telefono
            if rfc:
                trabajador.rfc = rfc
            if rol_codigo:
                rol = models.Rol.objects.get(codigo=rol_codigo)
                trabajador.rol = rol
            
            trabajador.save()
            
            messages.success(request, f'Trabajador "{trabajador.nombre}" actualizado correctamente')
            return HttpResponseRedirect(reverse('trabajadores'))
            
        except models.Trabajador.DoesNotExist:
            messages.error(request, 'Trabajador no encontrado')
            return HttpResponseRedirect(reverse('trabajadores'))
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return HttpResponseRedirect(reverse('trabajadores'))
    
    return HttpResponseRedirect(reverse('trabajadores'))


class Trabajadores(generic.ListView):
    template_name = "BookingRoomApp/administracion/trabajadores.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        if rol != "ADMIN":
            return HttpResponseRedirect(reverse("home"))

        trabajadores_list = models.Trabajador.objects.select_related("cuenta", "rol")
        roles = models.Rol.objects.all()
        trabajador_total = models.Trabajador.objects.count()

        nombre = request.GET.get('nombre', '')
        no_empleado = request.GET.get('no_empleado', '')
        rol_filtro = request.GET.get('rol', '')
        
        if nombre:
            trabajadores_list = trabajadores_list.filter(
                Q(nombre__icontains=nombre) |
                Q(apellidoPaterno__icontains=nombre) |
                Q(apelidoMaterno__icontains=nombre)
            )
        
        if no_empleado:
            trabajadores_list = trabajadores_list.filter(no_empleado__icontains=no_empleado)
        
        if rol_filtro:
            trabajadores_list = trabajadores_list.filter(rol_id=rol_filtro)

        trabajadores_list = trabajadores_list.all()

        return render(
            request,
            self.template_name,
            {
                "roles": roles,
                "trabajadores": trabajadores_list,
                "rol": rol,
                "nombre": nombre,
                "no_empleado": no_empleado,
                "rol_filtro": rol_filtro,
                "trabajador_total": trabajador_total
            },
        )


def trabajadores(request):
    return HttpResponseRedirect(reverse("trabajadores"))


def registrar_trabajador(request):
    estado_cuenta = models.EstadoCuenta.objects.filter(codigo="ACT").first()

    if request.method == "POST":
        form_tipo = request.POST.get("form_tipo")

        if form_tipo == "cuenta":
            nombre_usuario = request.POST.get("nombre_usuario")
            email = request.POST.get("email")
            contrasena = request.POST.get("contrasena")
            confirmar_contrasena = request.POST.get("confirmar_contrasena")

            if contrasena != confirmar_contrasena:
                messages.error(request, "Las contraseñas no coinciden")
                return HttpResponseRedirect(reverse("trabajadores"))

            request.session["cuenta_data"] = {
                "nombre_usuario": nombre_usuario,
                "email": email,
                "contrasena": contrasena,
            }
            messages.success(
                request,
                "Datos de cuenta guardados. Complete los datos del trabajador para poder registrarlo en el sitema.",
            )
            return HttpResponseRedirect(reverse("trabajadores"))

        elif form_tipo == "trabajador":
            cuenta_data = request.session.get("cuenta_data")
            if not cuenta_data:
                messages.error(request, "Primero complete los datos de la cuenta")
                return HttpResponseRedirect(reverse("trabajadores"))

            no_empleado = request.POST.get("no_empleado")
            rfc = request.POST.get("rfc")
            nombre = request.POST.get("nombre")
            apellido_paterno = request.POST.get("apellido_paterno")
            apellido_materno = request.POST.get("apellido_materno")
            telefono = request.POST.get("telefono")
            rol_id = request.POST.get("rol_id")

            try:
                firebase_uid = None
                if FIREBASE_ENABLED:
                    try:
                        firebase_user = auth.create_user(
                            email=cuenta_data["email"],
                            password=cuenta_data["contrasena"],
                            display_name=cuenta_data["nombre_usuario"],
                        )
                        firebase_uid = firebase_user.uid
                    except Exception as e:
                        messages.warning(request, f"Firebase no disponible: {str(e)}")

                cuenta = models.Cuenta.objects.create(
                    nombre_usuario=cuenta_data["nombre_usuario"],
                    correo_electronico=cuenta_data["email"],
                    firebase_uid=firebase_uid,
                    estado_cuenta=estado_cuenta,
                    disposicion=True,
                )

                models.Trabajador.objects.create(
                    no_empleado=no_empleado,
                    rfc=rfc,
                    nombre_fiscal=f"{nombre} {apellido_paterno} {apellido_materno}",
                    nombre=nombre,
                    apellidoPaterno=apellido_paterno,
                    apelidoMaterno=apellido_materno,
                    telefono=telefono,
                    correo_electronico=cuenta_data["email"],
                    rol_id=rol_id,
                    cuenta=cuenta,
                )

                del request.session["cuenta_data"]
                messages.success(request, "Trabajador registrado exitosamente")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                if FIREBASE_ENABLED and firebase_uid:
                    try:
                        auth.delete_user(firebase_uid)
                    except:
                        pass

    return HttpResponseRedirect(reverse("trabajadores"))


class Salones(generic.ListView):
    template_name = "BookingRoomApp/administracion/salones.html"
    context_object_name = "salones"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        salones = models.Salon.objects.select_related("estado_salon")
        estados = models.EstadoSalon.objects.all()
        salon_total = models.Salon.objects.count()

        nombre = request.GET.get('nombre', '')
        estado = request.GET.get('estado', '')
        orden = request.GET.get('orden', '')
        
        if nombre:
            salones = salones.filter(nombre__icontains=nombre)
        
        if estado:
            salones = salones.filter(estado_salon_id=estado)
        
        if orden == 'costo_asc':
            salones = salones.order_by('costo')
        elif orden == 'costo_desc':
            salones = salones.order_by('-costo')
        elif orden == 'nombre':
            salones = salones.order_by('nombre')
        else:
            salones = salones.order_by('-id')

        salones = salones.all()

        return render(
            request,
            self.template_name,
            {
                "salones": salones,
                "estados": estados,
                "rol": rol,
                "nombre": nombre,
                "estado": estado,
                "orden": orden,
                "salon_total": salon_total
            },
        )



    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        form_salones = request.POST.get("form_salones")

        if form_salones == "salon":
            nombre = request.POST.get("nameSalon")
            costo = request.POST.get("costoSalon")
            ubicacion = request.POST.get("ubicacionSalon")
            altura = request.POST.get("alturaSalon")
            ancho = request.POST.get("anchoSalon")
            largo = request.POST.get("largoSalon")
            metros = request.POST.get("meCuadra")

            models.Salon.objects.create(
                nombre=nombre,
                costo=costo,
                ubicacion=ubicacion,
                dimenLargo=largo,
                dimenAncho=ancho,
                dimenAlto=altura,
                metrosCuadrados=metros,
                maxCapacidad=50,
                estado_salon=models.EstadoSalon.objects.get(codigo="DIS"),
            )

            messages.success(request, f'El salón: {nombre} fue registrado exitosamente')

        return HttpResponseRedirect(reverse("salones"))



class Mobiliarios(generic.ListView):
    template_name = "BookingRoomApp/administracion/mobiliario.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        mobiliarios = models.Mobiliario.objects.select_related('tipo_movil').prefetch_related('descripcion_mob')
        tipos_mobil = models.TipoMobil.objects.filter(disposicion=True)
        mobiliario_total = models.Mobiliario.objects.count()

        nombre = request.GET.get('nombre', '')
        tipo = request.GET.get('tipo', '')
        orden = request.GET.get('orden', '')
        
        if nombre:
            mobiliarios = mobiliarios.filter(nombre__icontains=nombre)
        
        if tipo:
            mobiliarios = mobiliarios.filter(tipo_movil_id=tipo)
        
        if orden == 'costo_asc':
            mobiliarios = mobiliarios.order_by('costo')
        elif orden == 'costo_desc':
            mobiliarios = mobiliarios.order_by('-costo')
        else:
            mobiliarios = mobiliarios.order_by('-id')

        mobiliarios = mobiliarios.all()

        return render(request, self.template_name, {
            'mobiliarios': mobiliarios,
            'tipos_mobil': tipos_mobil,
            'rol': rol,
            'nombre': nombre,
            'orden': orden,
            'mobiliario_total': mobiliario_total
        })

    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        form_mobiliarios = request.POST.get("form_mobiliarios")

        if form_mobiliarios == "mobiliario":
            nombre = request.POST.get("nameMobiliario")
            descripcion = request.POST.get("descripcion")
            costo = request.POST.get("costoMobiliario")
            stock = request.POST.get("stockTotal")
            tipo_mobil_id = request.POST.get("tipo_mobil")
            cantidad_caracteristicas = int(request.POST.get("cantidad_caracteristicas", 0))
            
            tipo_mobil = models.TipoMobil.objects.get(pk=tipo_mobil_id)
            
            mobiliario = models.Mobiliario.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                costo=costo,
                stock=stock,
                tipo_movil=tipo_mobil,
            )
            
            for i in range(1, cantidad_caracteristicas + 1):
                caracteristica_desc = request.POST.get(f"caracteristica_{i}")
                if caracteristica_desc:
                    caracteristica, created = models.CaracterMobil.objects.get_or_create(
                        descripcion=caracteristica_desc
                    )
                    mobiliario.descripcion_mob.add(caracteristica)
            
            messages.success(request, f'El mobiliario: {nombre} fue registrado exitosamente')
        
        return HttpResponseRedirect(reverse("mobiliario"))


class Equipamientos(generic.ListView):
    template_name = "BookingRoomApp/administracion/equipamiento.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        equipamientos = models.Equipamiento.objects.select_related("tipo_equipa")
        tipos_equipa = models.TipoEquipa.objects.filter(disposicion=True)
        equipamiento_total = models.Equipamiento.objects.count()

        nombre = request.GET.get('nombre', '')
        tipo = request.GET.get('tipo', '')
        orden = request.GET.get('orden', '')
        
        if nombre:
            equipamientos = equipamientos.filter(nombre__icontains=nombre)
        
        if tipo:
            equipamientos = equipamientos.filter(tipo_equipa_id=tipo)
        
        if orden == 'costo_asc':
            equipamientos = equipamientos.order_by('costo')
        elif orden == 'costo_desc':
            equipamientos = equipamientos.order_by('-costo')
        else:
            equipamientos = equipamientos.order_by('-id')

        equipamientos = equipamientos.all()

        return render(
            request,
            self.template_name,
            {
                "equipamientos": equipamientos,
                "tipos_equipa": tipos_equipa,
                "rol": rol,
                'nombre': nombre,
                'orden': orden,
                'equipamiento_total': equipamiento_total
            },
        )
    

    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        form_equipamiento = request.POST.get("form_equipamiento")

        if form_equipamiento == "equipamiento":
            nombre = request.POST.get("nameEquipamiento")
            descripcion = request.POST.get("descripcion")
            costo = request.POST.get("costoEquipamiento")
            stock = request.POST.get("stockEquipamiento")
            tipo_equipa_id = request.POST.get("tipo_equipa")

            tipo_equipa = models.TipoEquipa.objects.get(pk=tipo_equipa_id)

            models.Equipamiento.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                costo=costo,
                stock=stock,
                tipo_equipa=tipo_equipa,
            )

            messages.success(request, f'El equipamiento: {nombre} fue registrado exitosamente')

        return HttpResponseRedirect(reverse("equipamiento"))


# def historial_reservacion(request):
#     cuenta, rol = get_cuenta_and_rol(request)
#     if not cuenta:
#         return HttpResponseRedirect(reverse('login'))

#     return render(request, 'BookingRoomApp/recepcion/historial_reservacion.html', {'rol': rol})


def inventario_equipamiento(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    return render(
        request, "BookingRoomApp/almacen/inventario_equipamiento.html", {"rol": rol}
    )


def inventario_mobiliario(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    return render(
        request, "BookingRoomApp/almacen/inventario_mobiliario.html", {"rol": rol}
    )


def pagos(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "BookingRoomApp/recepcion/pagos.html", {"rol": rol})


def estadisticas(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    return render(
        request, "BookingRoomApp/administracion/estadisticas.html", {"rol": rol}
    )


@csrf_exempt
def actualizar_reservacion(request, pk):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                reservacion = models.Reservacion.objects.select_related('cliente').get(pk=pk)
                cliente = reservacion.cliente

                if request.POST.get('cliente_nombre'):
                    cliente.nombre = request.POST.get('cliente_nombre')
                if request.POST.get('cliente_apellido_paterno'):
                    cliente.apellidoPaterno = request.POST.get('cliente_apellido_paterno')
                if request.POST.get('cliente_apellido_materno'):
                    cliente.apelidoMaterno = request.POST.get('cliente_apellido_materno')
                if request.POST.get('cliente_correo'):
                    cliente.correo_electronico = request.POST.get('cliente_correo')
                if request.POST.get('cliente_telefono'):
                    cliente.telefono = request.POST.get('cliente_telefono')
                if request.POST.get('cliente_rfc'):
                    cliente.rfc = request.POST.get('cliente_rfc')
                if request.POST.get('cliente_nombre_fiscal'):
                    cliente.nombre_fiscal = request.POST.get('cliente_nombre_fiscal')
                cliente.save()

                if request.POST.get('evento_nombre'):
                    reservacion.nombreEvento = request.POST.get('evento_nombre')
                if request.POST.get('evento_descripcion'):
                    reservacion.descripEvento = request.POST.get('evento_descripcion')
                if request.POST.get('evento_fecha'):
                    reservacion.fechaEvento = request.POST.get('evento_fecha')
                if request.POST.get('evento_hora_inicio'):
                    reservacion.horaInicio = request.POST.get('evento_hora_inicio')
                if request.POST.get('evento_hora_fin'):
                    reservacion.horaFin = request.POST.get('evento_hora_fin')
                if request.POST.get('evento_asistentes'):
                    reservacion.estimaAsistentes = request.POST.get('evento_asistentes')

                estado_codigo = request.POST.get('evento_estado', '')
                if estado_codigo:
                    estado = models.EstadoReserva.objects.get(codigo=estado_codigo)
                    reservacion.estado_reserva = estado

                reservacion.save()

            messages.success(request, 'Reservación actualizada correctamente')
            return JsonResponse({'success': True, 'redirect': reverse('historial_reservacion')})
        except models.Reservacion.DoesNotExist:
            messages.error(request, 'Reservación no encontrada')
            return JsonResponse({'success': False, 'message': 'Reservación no encontrada'}, status=404)
        except models.EstadoReserva.DoesNotExist:
            messages.error(request, 'Estado no encontrado')
            return JsonResponse({'success': False, 'message': 'Estado no encontrado'}, status=400)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)
