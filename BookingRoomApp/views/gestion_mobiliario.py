import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


class Mobiliarios(generic.ListView):
    template_name = "BookingRoomApp/administracion/mobiliario.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        mobiliarios = models.Mobiliario.objects.select_related('tipo_movil').prefetch_related('descripcion_mob')
        tipos_mobil = models.TipoMobil.objects.filter(disposicion=True)

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

        return render(request, self.template_name, {
            'mobiliarios': mobiliarios.all(),
            'tipos_mobil': tipos_mobil,
            'rol': rol,
            'nombre': nombre, 
            'orden': orden,
            'mobiliario_total': models.Mobiliario.objects.count()
        })

    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        if request.POST.get("form_mobiliarios") == "mobiliario":
            tipo_mobil = get_object_or_404(models.TipoMobil, pk=request.POST.get("tipo_mobil"))
            
            mobiliario = models.Mobiliario.objects.create(
                nombre=request.POST.get("nameMobiliario"),
                descripcion=request.POST.get("descripcion"),
                costo=request.POST.get("costoMobiliario"),
                stock=request.POST.get("stockTotal"),
                tipo_movil=tipo_mobil,
            )
            
            cantidad_caracteristicas = int(request.POST.get("cantidad_caracteristicas", 0))
            for i in range(1, cantidad_caracteristicas + 1):
                caracteristica_desc = request.POST.get(f"caracteristica_{i}")
                if caracteristica_desc:
                    caracteristica, _ = models.CaracterMobil.objects.get_or_create(descripcion=caracteristica_desc)
                    mobiliario.descripcion_mob.add(caracteristica)
            
            estado_inicial = models.EstadoMobil.objects.filter(codigo="DISP").first()
            if not estado_inicial:
                estado_inicial = models.EstadoMobil.objects.first()
            
            if estado_inicial:
                models.InventarioMob.objects.create(
                    mobiliario=mobiliario,
                    estado_mobil=estado_inicial,
                    cantidad=request.POST.get("stockTotal")
                )
            
            messages.success(request, 'Mobiliario registrado exitosamente')
        
        return HttpResponseRedirect(reverse("mobiliario"))


def actualizar_mobiliario(request, pk):
    if request.method == 'POST':
        try:
            mobiliario = get_object_or_404(models.Mobiliario, pk=pk)
            stock_anterior = mobiliario.stock
            
            if request.POST.get('nombre'):
                mobiliario.nombre = request.POST.get('nombre')
            if request.POST.get('descripcion'):
                mobiliario.descripcion = request.POST.get('descripcion')
            if request.POST.get('costo'):
                mobiliario.costo = request.POST.get('costo')
            if request.POST.get('stock'):
                nuevo_stock = int(request.POST.get('stock'))
                diferencia = nuevo_stock - stock_anterior
                mobiliario.stock = nuevo_stock
                
                # Sincronizar con InventarioMob
                if diferencia != 0:
                    estado_disp = models.EstadoMobil.objects.filter(codigo="DISP").first()
                    if not estado_disp:
                        estado_disp = models.EstadoMobil.objects.first()
                    
                    if estado_disp:
                        inv_disp, created = models.InventarioMob.objects.get_or_create(
                            mobiliario=mobiliario,
                            estado_mobil=estado_disp,
                            defaults={'cantidad': 0}
                        )
                        inv_disp.cantidad += diferencia
                        if inv_disp.cantidad < 0:
                            inv_disp.cantidad = 0
                        inv_disp.save()

            if request.POST.get('tipo_movil'):
                mobiliario.tipo_movil = models.TipoMobil.objects.get(pk=request.POST.get('tipo_movil'))
            
            mobiliario.save()
            messages.success(request, 'Mobiliario actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return HttpResponseRedirect(reverse('mobiliario'))





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



    return render(
        request,
        "BookingRoomApp/almacen/inventario_mobiliario.html",
        {
            "inventario": inventario,
            "rol": rol,
            "estados": models.EstadoMobil.objects.all(),
            "tipos": models.TipoMobil.objects.all()
        }
    )


def actualizar_estado_mobiliario(request):
    if request.method == "POST":
        inventario_id = request.POST.get("inventario_id")
        cantidad_a_mover = int(request.POST.get("cantidad", 0))
        estado_codigo = request.POST.get("estado")

        if not inventario_id or cantidad_a_mover <= 0:
            return redirect("inventario_mobiliario")

        inv_origen = get_object_or_404(models.InventarioMob, id=inventario_id)
        nuevo_estado = get_object_or_404(models.EstadoMobil, codigo=estado_codigo)

        cantidad_a_mover = min(cantidad_a_mover, inv_origen.cantidad)
        inv_origen.cantidad -= cantidad_a_mover

        if inv_origen.cantidad == 0:
            inv_origen.delete()
        else:
            inv_origen.save()

        inv_destino, _ = models.InventarioMob.objects.get_or_create(
            mobiliario=inv_origen.mobiliario,
            estado_mobil=nuevo_estado,
            defaults={"cantidad": 0}
        )
        inv_destino.cantidad += cantidad_a_mover
        inv_destino.save()

    return redirect("inventario_mobiliario")


def mobiliario_caracteristicas(request, pk):
    if request.method == 'GET':
        try:
            mobiliario = models.Mobiliario.objects.select_related('tipo_movil').get(pk=pk)
            caracteristicas = list(mobiliario.descripcion_mob.values_list('descripcion', flat=True))
            return JsonResponse({
                'nombre': mobiliario.nombre,
                'tipo': mobiliario.tipo_movil.nombre if mobiliario.tipo_movil else '',
                'descripcion': mobiliario.descripcion,
                'caracteristicas': caracteristicas
            })
        except models.Mobiliario.DoesNotExist:
            return JsonResponse({'error': 'Mobiliario no encontrado'}, status=404)
    
    elif request.method == 'POST':
        try:
            mobiliario = get_object_or_404(models.Mobiliario, pk=pk)
            data = json.loads(request.body)
            caracteristicas_nuevas = data.get('caracteristicas', [])
            
            mobiliario.descripcion_mob.clear()
            for desc in caracteristicas_nuevas:
                if desc.strip():
                    caracteristica, _ = models.CaracterMobil.objects.get_or_create(descripcion=desc.strip())
                    mobiliario.descripcion_mob.add(caracteristica)
            
            return JsonResponse({'success': True, 'message': 'Características actualizadas'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def obtener_resumen_estados_mob(request, inventario_id):
    try:
        item_base = get_object_or_404(models.InventarioMob, pk=inventario_id)
        resumen = models.InventarioMob.objects.filter(
            mobiliario=item_base.mobiliario
        ).values('estado_mobil__nombre', 'cantidad')
        
        return JsonResponse({
            'status': 'success', 
            'nombre_mob': item_base.mobiliario.nombre,
            'data': list(resumen)
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def api_lista_mobiliario(request):
    data_final = []
    items = models.Mobiliario.objects.all()
    for item in items:
        estados = models.InventarioMob.objects.filter(mobiliario=item, cantidad__gt=0)
        data_final.append({
            "id": item.id,
            "nombre": item.nombre,
            "tipo": item.tipo_movil.nombre if item.tipo_movil else "N/A",
            "estados": [
                {
                    "id_inventario": est.id,
                    "nombre_estado": est.estado_mobil.nombre,
                    "codigo_estado": est.estado_mobil.codigo,
                    "cantidad": est.cantidad
                } for est in estados
            ]
        })
    return JsonResponse(data_final, safe=False)


@csrf_exempt
def api_mover_mobiliario(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            inv_id = data.get("inventario_id")
            cant = int(data.get("cantidad", 0))
            nuevo_estado_cod = data.get("nuevo_estado_codigo")

            if cant <= 0:
                return JsonResponse({"error": "Cantidad debe ser mayor a 0"}, status=400)

            inv_origen = get_object_or_404(models.InventarioMob, id=inv_id)
            nuevo_estado = get_object_or_404(models.EstadoMobil, codigo=nuevo_estado_cod)

            cant = min(cant, inv_origen.cantidad)
            inv_origen.cantidad -= cant
            
            if inv_origen.cantidad == 0:
                inv_origen.delete()
            else:
                inv_origen.save()

            inv_destino, _ = models.InventarioMob.objects.get_or_create(
                mobiliario=inv_origen.mobiliario,
                estado_mobil=nuevo_estado,
                defaults={"cantidad": 0}
            )
            inv_destino.cantidad += cant
            inv_destino.save()

            return JsonResponse({"success": True, "message": "Movimiento exitoso"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
    return JsonResponse({"error": "Método no permitido"}, status=405)


def api_estados_mobiliario(request):
    try:
        estados = models.EstadoMobil.objects.values('codigo', 'nombre')
        return JsonResponse(list(estados), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)