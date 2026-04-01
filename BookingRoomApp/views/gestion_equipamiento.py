from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


class Equipamientos(generic.ListView):
    template_name = "BookingRoomApp/administracion/equipamiento.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        equipamientos = models.Equipamiento.objects.select_related("tipo_equipa")
        tipos_equipa = models.TipoEquipa.objects.filter(disposicion=True)

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

        return render(request, self.template_name, {
            "equipamientos": equipamientos.order_by('-id').all(),
            "tipos_equipa": tipos_equipa,
            "rol": rol,
            "nombre": nombre, "orden": orden,
            "equipamiento_total": models.Equipamiento.objects.count(),
        })
    

    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        if request.POST.get("form_equipamiento") == "equipamiento":
            models.Equipamiento.objects.create(
                nombre=request.POST.get("nameEquipamiento"),
                descripcion=request.POST.get("descripcion"),
                costo=request.POST.get("costoEquipamiento"),
                stock=request.POST.get("stockEquipamiento"),
                tipo_equipa=models.TipoEquipa.objects.get(pk=request.POST.get("tipo_equipa")),
            )
            messages.success(request, f'Equipamiento registrado exitosamente')

        return HttpResponseRedirect(reverse("equipamiento"))


def actualizar_equipamiento(request, pk):
    if request.method == 'POST':
        try:
            equipamiento = models.Equipamiento.objects.get(pk=pk)
            if request.POST.get('nombre'):
                equipamiento.nombre = request.POST.get('nombre')
            if request.POST.get('descripcion'):
                equipamiento.descripcion = request.POST.get('descripcion')
            if request.POST.get('costo'):
                equipamiento.costo = request.POST.get('costo')
            if request.POST.get('stock'):
                equipamiento.stock = request.POST.get('stock')
            if request.POST.get('tipo_equipa'):
                equipamiento.tipo_equipa = models.TipoEquipa.objects.get(pk=request.POST.get('tipo_equipa'))
            equipamiento.save()
            messages.success(request, f'Equipamiento actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return HttpResponseRedirect(reverse('equipamiento'))


def inventario_equipamiento(request):
    cuenta, rol = get_cuenta_and_rol(request)
    if not cuenta:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "BookingRoomApp/almacen/inventario_equipamiento.html", {"rol": rol})