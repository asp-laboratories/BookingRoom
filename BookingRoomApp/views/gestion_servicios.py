from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


class Servicios(generic.ListView):
    template_name = "BookingRoomApp/administracion/servicios.html"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))
        
        servicios = models.Servicio.objects.select_related("tipo_servicio")
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

        return render(request, self.template_name, {
            "servicios": servicios.all(),
            "tipo_servicio": tipo_servicio,
            "rol": rol,
            "nombre": nombre, "orden": orden, "disposicion": disposicion,
            "servicio_total": models.Servicio.objects.count(),
        })

    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        if request.POST.get("form_servicios") == "servicio":
            models.Servicio.objects.create(
                nombre=request.POST.get("nameServicio"),
                descripcion=request.POST.get("descripcion"),
                costo=request.POST.get("costoServicio"),
                disposicion=True,
                tipo_servicio=models.TipoServicio.objects.get(pk=request.POST.get("tipo_servicio")),
            )
            messages.success(request, f'Servicio registrado exitosamente')

        return HttpResponseRedirect(reverse("servicios"))


def actualizar_servicio(request, pk):
    if request.method == 'POST':
        try:
            servicio = models.Servicio.objects.get(pk=pk)
            if request.POST.get('nombre'):
                servicio.nombre = request.POST.get('nombre')
            if request.POST.get('descripcion'):
                servicio.descripcion = request.POST.get('descripcion')
            if request.POST.get('costo'):
                servicio.costo = request.POST.get('costo')
            if request.POST.get('tipo_servicio'):
                servicio.tipo_servicio = models.TipoServicio.objects.get(pk=request.POST.get('tipo_servicio'))
            servicio.disposicion = request.POST.get('disposicion') == 'true'
            servicio.save()
            messages.success(request, f'Servicio actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return HttpResponseRedirect(reverse('servicios'))


def servicios(request):
    return HttpResponseRedirect(reverse("servicios"))


def crear_tipo(request):
    from django.http import JsonResponse
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        nombre = request.POST.get('nombre_tipo')
        disposicion = request.POST.get('disposicion') == 'on'
        
        try:
            if tipo == 'servicio':
                models.TipoServicio.objects.create(nombre=nombre, disposicion=disposicion)
            elif tipo == 'equipamiento':
                models.TipoEquipa.objects.create(nombre=nombre, disposicion=disposicion)
            elif tipo == 'mobiliario':
                models.TipoMobil.objects.create(nombre=nombre, disposicion=disposicion)
            elif tipo == 'montaje':
                models.TipoMontaje.objects.create(nombre=nombre, disposicion=disposicion)
            else:
                return JsonResponse({'success': False, 'message': 'Tipo no válido'}, status=400)
            
            return JsonResponse({'success': True, 'message': f'Tipo {nombre} creado exitosamente'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)