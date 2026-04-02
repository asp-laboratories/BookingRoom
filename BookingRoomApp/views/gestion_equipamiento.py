from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
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
            tipo_equipa = models.TipoEquipa.objects.get(pk=request.POST.get("tipo_equipa"))
            nuevo_equipamiento = models.Equipamiento.objects.create(
                nombre=request.POST.get("nameEquipamiento"),
                descripcion=request.POST.get("descripcion"),
                costo=request.POST.get("costoEquipamiento"),
                stock=request.POST.get("stockEquipamiento"),
                tipo_equipa=tipo_equipa,
            )
            
            estado_inicial = models.EstadoEquipa.objects.filter(codigo="DISP").first()
            if not estado_inicial:
                estado_inicial = models.EstadoEquipa.objects.first()
            
            if estado_inicial:
                models.InventarioEquipa.objects.create(
                    equipamiento=nuevo_equipamiento,
                    estado_equipa=estado_inicial,
                    cantidad=request.POST.get("stockEquipamiento")
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
        from django.shortcuts import get_object_or_404
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