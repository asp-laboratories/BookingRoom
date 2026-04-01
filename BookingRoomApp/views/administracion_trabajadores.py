from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol

try:
    import firebase_admin
    from firebase_admin import auth
    FIREBASE_ENABLED = True
except:
    FIREBASE_ENABLED = False


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

        nombre = request.GET.get('nombre', '')
        no_empleado = request.GET.get('no_empleado', '')
        rol_filtro = request.GET.get('rol', '')
        
        if nombre:
            trabajadores_list = trabajadores_list.filter(
                Q(nombre__icontains=nombre) | Q(apellidoPaterno__icontains=nombre) | Q(apelidoMaterno__icontains=nombre)
            )
        if no_empleado:
            trabajadores_list = trabajadores_list.filter(no_empleado__icontains=no_empleado)
        if rol_filtro:
            trabajadores_list = trabajadores_list.filter(rol_id=rol_filtro)

        return render(request, self.template_name, {
            "roles": roles,
            "trabajadores": trabajadores_list.order_by('-no_empleado').all(),
            "rol": rol,
            "nombre": nombre, "no_empleado": no_empleado, "rol_filtro": rol_filtro,
            "trabajador_total": models.Trabajador.objects.count()
        })


def trabajadores(request):
    return HttpResponseRedirect(reverse("trabajadores"))


def registrar_trabajador(request):
    estado_cuenta = models.EstadoCuenta.objects.filter(codigo="ACT").first()

    if request.method == "POST":
        form_tipo = request.POST.get("form_tipo")

        if form_tipo == "cuenta":
            if request.POST.get("contrasena") != request.POST.get("confirmar_contrasena"):
                messages.error(request, "Las contraseñas no coinciden")
                return HttpResponseRedirect(reverse("trabajadores"))

            request.session["cuenta_data"] = {
                "nombre_usuario": request.POST.get("nombre_usuario"),
                "email": request.POST.get("email"),
                "contrasena": request.POST.get("contrasena"),
            }
            messages.success(request, "Datos de cuenta guardados. Complete los datos del trabajador.")
            return HttpResponseRedirect(reverse("trabajadores"))

        elif form_tipo == "trabajador":
            cuenta_data = request.session.get("cuenta_data")
            if not cuenta_data:
                messages.error(request, "Primero complete los datos de la cuenta")
                return HttpResponseRedirect(reverse("trabajadores"))

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
                    no_empleado=request.POST.get("no_empleado"),
                    rfc=request.POST.get("rfc"),
                    nombre_fiscal=f"{request.POST.get('nombre')} {request.POST.get('apellido_paterno')} {request.POST.get('apellido_materno')}",
                    nombre=request.POST.get("nombre"),
                    apellidoPaterno=request.POST.get("apellido_paterno"),
                    apelidoMaterno=request.POST.get("apellido_materno"),
                    telefono=request.POST.get("telefono"),
                    correo_electronico=cuenta_data["email"],
                    rol_id=request.POST.get("rol_id"),
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


def actualizar_trabajador(request, pk):
    if request.method == 'POST':
        try:
            trabajador = models.Trabajador.objects.get(pk=pk)
            if request.POST.get('nombre'):
                trabajador.nombre = request.POST.get('nombre')
            if request.POST.get('apellidoPaterno'):
                trabajador.apellidoPaterno = request.POST.get('apellidoPaterno')
            if request.POST.get('apellidoMaterno'):
                trabajador.apelidoMaterno = request.POST.get('apellidoMaterno')
            if request.POST.get('telefono'):
                trabajador.telefono = request.POST.get('telefono')
            if request.POST.get('rfc'):
                trabajador.rfc = request.POST.get('rfc')
            if request.POST.get('rol'):
                trabajador.rol = models.Rol.objects.get(codigo=request.POST.get('rol'))
            trabajador.save()
            messages.success(request, f'Trabajador actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return HttpResponseRedirect(reverse('trabajadores'))