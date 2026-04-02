from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
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
    context = {}

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        reservaciones = models.Reservacion.objects.select_related(
            "cliente",
            "estado_reserva",
            "montaje__salon",
        )

        self.context = {"reservaciones": reservaciones, "rol": rol}

        return render(request, self.template_name, self.context)


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
        
        servicios = models.Servicio.objects.select_related('tipo_servicio').all()
        tipo_servicio = models.TipoServicio.objects.filter(disposicion=True)

        return render(request, self.template_name, {
            'servicios': servicios,
            'tipo_servicio': tipo_servicio,
            'rol': rol
        })


def servicios(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))
    
    if request.method == "POST":
        form_servicios = request.POST.get('form_servicios')

        if form_servicios == "servicio":
            nombre = request.POST.get('nameServicio')
            descripcion = request.POST.get('descripcion')
            costo = request.POST.get('costoServicio')
            tipo_servicio_id = request.POST.get('tipo_servicio')
            
            tipo_servicio = models.TipoServicio.objects.get(pk=tipo_servicio_id)

            models.Servicio.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                costo=costo,
                disposicion=True,
                tipo_servicio=tipo_servicio
            )
    
    return HttpResponseRedirect(reverse("servicios"))






def trabajadores(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    if rol != "ADMIN":
        return HttpResponseRedirect(reverse("home"))

    roles = models.Rol.objects.all()
    trabajadores_list = models.Trabajador.objects.select_related("cuenta", "rol").all()

    return render(
        request,
        "BookingRoomApp/administracion/trabajadores.html",
        {"roles": roles, "trabajadores": trabajadores_list, "rol": rol},
    )


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
    context_object_name = 'salones'
    
    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        salones = models.Salon.objects.select_related('estado_salon').all()
        estados = models.EstadoSalon.objects.all()
        
        return render(request, self.template_name, {
            'salones': salones,
            'estados': estados,
            'rol': rol
        })



def registrar_salones(request):
    if request.method == "POST":
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
                estado_salon="ACT",
            )


def mobiliario(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))

    return render(
        request, "BookingRoomApp/administracion/mobiliario.html", {"rol": rol}
    )


class Equipamientos(generic.ListView):
    template_name = "BookingRoomApp/administracion/equipamiento.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        equipamientos = models.Equipamiento.objects.select_related('tipo_equipa').all()
        tipos_equipa = models.TipoEquipa.objects.filter(disposicion=True)

        return render(request, self.template_name, {
            'equipamientos': equipamientos,
            'tipos_equipa': tipos_equipa,
            'rol': rol
        })


def equipamiento(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return redirect("login")

    if request.method == "POST":
        form_equipamiento = request.POST.get('form_equipamiento')

        if form_equipamiento == "equipamiento":
            nombre = request.POST.get('nameEquipamiento')
            descripcion = request.POST.get('descripcion')
            costo = float(request.POST.get('costoEquipamiento', 0))
            stock = int(request.POST.get('stockEquipamiento', 0))
            tipo_equipa_id = request.POST.get('tipo_equipa')

            tipo_equipa = get_object_or_404(models.TipoEquipa, pk=tipo_equipa_id)

            nuevo_equipamiento = models.Equipamiento.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                costo=costo,
                stock=stock,
                tipo_equipa=tipo_equipa
            )

            estado_inicial = get_object_or_404(models.EstadoEquipa, codigo="DISP")
            models.InventarioEquipa.objects.create(
                equipamiento=nuevo_equipamiento,
                estado_equipa=estado_inicial,
                cantidad=stock
            )

    return redirect("equipamiento")

def inventario_equipamiento(request):
    cuenta, rol = get_cuenta_and_rol(request)
    
    if not cuenta:
        return redirect("login")

    inventario = models.InventarioEquipa.objects.select_related(
        "equipamiento",
        "equipamiento__tipo_equipa",
        "estado_equipa"
    ).filter(cantidad__gt=0)

    buscar = request.GET.get("buscar")
    estado = request.GET.get("estado")
    tipo = request.GET.get("tipo")

    if buscar:
        inventario = inventario.filter(equipamiento__nombre__icontains=buscar)
    if estado:
        inventario = inventario.filter(estado_equipa__codigo=estado)
    if tipo:
        inventario = inventario.filter(equipamiento__tipo_equipa__id=tipo)

    estados = models.EstadoEquipa.objects.all()
    tipos = models.TipoEquipa.objects.all()

    return render(
        request,
        "BookingRoomApp/almacen/inventario_equipamiento.html",
        {
            "inventario": inventario,
            "rol": rol,
            "estados": estados,
            "tipos": tipos
        }
    )


def actualizar_estado_equipamiento(request):
    if request.method == "POST":
        inventario_id = request.POST.get("inventario_id")
        cantidad = int(request.POST.get("cantidad", 0))
        estado_codigo = request.POST.get("estado")

        if not inventario_id or cantidad <= 0:
            return redirect("inventario_equipamiento")

        inventario = get_object_or_404(models.InventarioEquipa, id=inventario_id)
        nuevo_estado = get_object_or_404(models.EstadoEquipa, codigo=estado_codigo)

        cantidad = min(cantidad, inventario.cantidad)
        if cantidad == 0:
            return redirect("inventario_equipamiento")

        inventario.cantidad -= cantidad
        if inventario.cantidad == 0:
            inventario.delete()
        else:
            inventario.save()

        otro_inventario, creado = models.InventarioEquipa.objects.get_or_create(
            equipamiento=inventario.equipamiento,
            estado_equipa=nuevo_estado,
            defaults={"cantidad": 0}
        )
        
        otro_inventario.cantidad += cantidad
        otro_inventario.save()

    return redirect("inventario_equipamiento")


# def historial_reservacion(request):
#     cuenta, rol = get_cuenta_and_rol(request)
#     if not cuenta:
#         return HttpResponseRedirect(reverse('login'))

#     return render(request, 'BookingRoomApp/recepcion/historial_reservacion.html', {'rol': rol})

def inventario_mobiliario(request):
    cuenta, rol = get_cuenta_and_rol(request)

    if not cuenta:
        return redirect("login")

    inventario = models.InventarioMob.objects.select_related(
        "mobiliario",
        "mobiliario__tipo_movil",
        "estado_mobil"
    ).filter(cantidad__gt=0)

    buscar = request.GET.get("buscar")
    estado = request.GET.get("estado")
    tipo = request.GET.get("tipo")

    if buscar:
        inventario = inventario.filter(mobiliario__nombre__icontains=buscar)

    if estado:
        inventario = inventario.filter(estado_mobil__codigo=estado)

    if tipo:
        inventario = inventario.filter(mobiliario__tipo_movil__id=tipo)

    estados = models.EstadoMobil.objects.all()
    tipos = models.TipoMobil.objects.all()

    return render(
        request,
        "BookingRoomApp/almacen/inventario_mobiliario.html",
        {
            "inventario": inventario,
            "rol": rol,
            "estados": estados,
            "tipos": tipos
        }
    )
    
def actualizar_estado_mobiliario(request):
    if request.method == "POST":
        inventario_id = request.POST.get("inventario_id")
        cantidad = int(request.POST.get("cantidad", 0))
        estado_codigo = request.POST.get("estado")

        if not inventario_id or cantidad <= 0:
            return redirect("inventario_mobiliario")

        inventario = get_object_or_404(models.InventarioMob, id=inventario_id)
        nuevo_estado = get_object_or_404(models.EstadoMobil, codigo=estado_codigo)

        cantidad = min(cantidad, inventario.cantidad)

        inventario.cantidad -= cantidad

        if inventario.cantidad == 0:
            inventario.delete()
        else:
            inventario.save()

        otro_inventario, creado = models.InventarioMob.objects.get_or_create(
            mobiliario=inventario.mobiliario,
            estado_mobil=nuevo_estado,
            defaults={"cantidad": 0}
        )

        otro_inventario.cantidad += cantidad
        otro_inventario.save()

    return redirect("inventario_mobiliario")

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
