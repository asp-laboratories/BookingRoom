import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
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
        else:
            equipamientos = equipamientos.order_by('-id')

        return render(request, self.template_name, {
            "equipamientos": equipamientos.all(),
            "tipos_equipa": tipos_equipa,
            "rol": rol,
            "nombre": nombre, 
            "orden": orden,
            "equipamiento_total": models.Equipamiento.objects.count(),
        })
        

    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        if request.POST.get("form_equipamiento") == "equipamiento":
            tipo_equipa = get_object_or_404(models.TipoEquipa, pk=request.POST.get("tipo_equipa"))
            
            nuevo_equipamiento = models.Equipamiento.objects.create(
                nombre=request.POST.get("nameEquipamiento"),
                descripcion=request.POST.get("descripcion"),
                costo=request.POST.get("costoEquipamiento", 0),
                stock=request.POST.get("stockEquipamiento", 0),
                tipo_equipa=tipo_equipa,
            )
            
            estado_inicial = models.EstadoEquipa.objects.filter(codigo="DISP").first()
            if not estado_inicial:
                estado_inicial = models.EstadoEquipa.objects.first()
            
            if estado_inicial:
                models.InventarioEquipa.objects.create(
                    equipamiento=nuevo_equipamiento,
                    estado_equipa=estado_inicial,
                    cantidad=request.POST.get("stockEquipamiento", 0)
                )
            
            messages.success(request, 'Equipamiento registrado exitosamente')

        return HttpResponseRedirect(reverse("equipamiento"))


def actualizar_equipamiento(request, pk):
    if request.method == 'POST':
        try:
            equipamiento = get_object_or_404(models.Equipamiento, pk=pk)
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
            messages.success(request, 'Equipamiento actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return HttpResponseRedirect(reverse('equipamiento'))




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
        
    return render(
        request,
        "BookingRoomApp/almacen/inventario_equipamiento.html",
        {
            "inventario": inventario,
            "rol": rol,
            "estados": models.EstadoEquipa.objects.all(),
            "tipos": models.TipoEquipa.objects.all()
        }
    )


def actualizar_estado_equipamiento(request):
    if request.method == "POST":
        inventario_id = request.POST.get("inventario_id")
        cantidad_a_mover = int(request.POST.get("cantidad", 0))
        estado_codigo = request.POST.get("estado")

        if not inventario_id or cantidad_a_mover <= 0:
            return redirect("inventario_equipamiento")

        inventario_origen = get_object_or_404(models.InventarioEquipa, id=inventario_id)
        nuevo_estado = get_object_or_404(models.EstadoEquipa, codigo=estado_codigo)

        cantidad_a_mover = min(cantidad_a_mover, inventario_origen.cantidad)
        
        inventario_origen.cantidad -= cantidad_a_mover
        if inventario_origen.cantidad == 0:
            inventario_origen.delete()
        else:
            inventario_origen.save()

        otro_inventario, _ = models.InventarioEquipa.objects.get_or_create(
            equipamiento=inventario_origen.equipamiento,
            estado_equipa=nuevo_estado,
            defaults={"cantidad": 0}
        )
        otro_inventario.cantidad += cantidad_a_mover
        otro_inventario.save()

    return redirect("inventario_equipamiento")

def obtener_resumen_estados(request, inventario_id):
    try:
        item_base = get_object_or_404(models.InventarioEquipa, pk=inventario_id)
        resumen = models.InventarioEquipa.objects.filter(
            equipamiento=item_base.equipamiento
        ).values('estado_equipa__nombre', 'cantidad')
        
        return JsonResponse({
            'status': 'success', 
            'nombre_equipo': item_base.equipamiento.nombre,
            'data': list(resumen)
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def api_lista_equipamiento(request):
    data_final = []
    items = models.Equipamiento.objects.all()
    
    for item in items:
        estados = models.InventarioEquipa.objects.filter(equipamiento=item, cantidad__gt=0)
        data_final.append({
            "id": item.id,
            "nombre": item.nombre,
            "tipo": item.tipo_equipa.nombre if item.tipo_equipa else "N/A",
            "estados": [
                {
                    "id_inventario": est.id,
                    "nombre_estado": est.estado_equipa.nombre,
                    "codigo_estado": est.estado_equipa.codigo,
                    "cantidad": est.cantidad
                } for est in estados
            ]
        })
    return JsonResponse(data_final, safe=False)


@csrf_exempt
def api_mover_equipamiento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            inv_id = data.get("inventario_id")
            cant = int(data.get("cantidad", 0))
            nuevo_estado_cod = data.get("nuevo_estado_codigo")

            if cant <= 0:
                return JsonResponse({"error": "Cantidad debe ser mayor a 0"}, status=400)

            inv_origen = get_object_or_404(models.InventarioEquipa, id=inv_id)
            nuevo_estado = get_object_or_404(models.EstadoEquipa, codigo=nuevo_estado_cod)

            cant = min(cant, inv_origen.cantidad)
            inv_origen.cantidad -= cant
            
            if inv_origen.cantidad == 0:
                inv_origen.delete()
            else:
                inv_origen.save()

            inv_destino, _ = models.InventarioEquipa.objects.get_or_create(
                equipamiento=inv_origen.equipamiento,
                estado_equipa=nuevo_estado,
                defaults={"cantidad": 0}
            )
            inv_destino.cantidad += cant
            inv_destino.save()

            return JsonResponse({"success": True, "message": "Movimiento exitoso"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
    return JsonResponse({"error": "Método no permitido"}, status=405)


def api_estados_equipamiento(request):
    try:
        estados = models.EstadoEquipa.objects.values('codigo', 'nombre')
        return JsonResponse(list(estados), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)