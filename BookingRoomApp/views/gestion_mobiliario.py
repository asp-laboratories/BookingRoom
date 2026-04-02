from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib import messages
from django.urls import reverse
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
            'nombre': nombre, 'orden': orden,
            'mobiliario_total': models.Mobiliario.objects.count()
        })

    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        if request.POST.get("form_mobiliarios") == "mobiliario":
            tipo_mobil = models.TipoMobil.objects.get(pk=request.POST.get("tipo_mobil"))
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
            
            try:
                estado_inicial = models.EstadoMobil.objects.filter(codigo="DISP").first()
                if not estado_inicial:
                    estado_inicial = models.EstadoMobil.objects.first()
                
                if estado_inicial:
                    models.InventarioMob.objects.create(
                        mobiliario=mobiliario,
                        estado_mobil=estado_inicial,
                        cantidad=request.POST.get("stockTotal")
                    )
            except Exception:
                pass
            
            messages.success(request, f'Mobiliario registrado exitosamente')
        
        return HttpResponseRedirect(reverse("mobiliario"))


def actualizar_mobiliario(request, pk):
    if request.method == 'POST':
        try:
            mobiliario = models.Mobiliario.objects.get(pk=pk)
            if request.POST.get('nombre'):
                mobiliario.nombre = request.POST.get('nombre')
            if request.POST.get('descripcion'):
                mobiliario.descripcion = request.POST.get('descripcion')
            if request.POST.get('costo'):
                mobiliario.costo = request.POST.get('costo')
            if request.POST.get('stock'):
                mobiliario.stock = request.POST.get('stock')
            if request.POST.get('tipo_movil'):
                mobiliario.tipo_movil = models.TipoMobil.objects.get(pk=request.POST.get('tipo_movil'))
            mobiliario.save()
            messages.success(request, f'Mobiliario actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return HttpResponseRedirect(reverse('mobiliario'))


# def inventario_mobiliario(request):
#     cuenta, rol = get_cuenta_and_rol(request)
#     if not cuenta:
#         return HttpResponseRedirect(reverse("login"))
#     return render(request, "BookingRoomApp/almacen/inventario_mobiliario.html", {"rol": rol})


def mobiliario_caracteristicas(request, pk):
    from django.http import JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    import json
    
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
            mobiliario = models.Mobiliario.objects.get(pk=pk)
            data = json.loads(request.body)
            caracteristicas_nuevas = data.get('caracteristicas', [])
            
            mobiliario.descripcion_mob.clear()
            
            for desc in caracteristicas_nuevas:
                if desc.strip():
                    caracteristica, created = models.CaracterMobil.objects.get_or_create(descripcion=desc.strip())
                    mobiliario.descripcion_mob.add(caracteristica)
            
            return JsonResponse({'success': True, 'message': 'Características actualizadas'})
        except models.Mobiliario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Mobiliario no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)



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