from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from BookingRoomApp import models
from BookingRoomApp.views import get_cuenta_and_rol


class Salones(generic.ListView):
    template_name = "BookingRoomApp/administracion/salones.html"
    context_object_name = "salones"

    def get(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        salones = models.Salon.objects.select_related("estado_salon")
        estados = models.EstadoSalon.objects.all()

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

        return render(request, self.template_name, {
            "salones": salones.order_by('-id').all(),
            "estados": estados,
            "rol": rol,
            "nombre": nombre, "estado": estado, "orden": orden,
            "salon_total": models.Salon.objects.count(),
        })


    def post(self, request):
        cuenta, rol = get_cuenta_and_rol(request)
        if not cuenta:
            return HttpResponseRedirect(reverse("login"))

        if request.POST.get("form_salones") == "salon":
            models.Salon.objects.create(
                nombre=request.POST.get("nameSalon"),
                costo=request.POST.get("costoSalon"),
                ubicacion=request.POST.get("ubicacionSalon"),
                dimenLargo=request.POST.get("largoSalon"),
                dimenAncho=request.POST.get("anchoSalon"),
                dimenAlto=request.POST.get("alturaSalon"),
                metrosCuadrados=request.POST.get("meCuadra"),
                maxCapacidad=50,
                estado_salon=models.EstadoSalon.objects.get(codigo="DIS"),
            )
            messages.success(request, f'Salón registrado exitosamente')

        return HttpResponseRedirect(reverse("salones"))


def actualizar_salon(request, pk):
    if request.method == 'POST':
        try:
            salon = models.Salon.objects.get(pk=pk)
            if request.POST.get('nombre'):
                salon.nombre = request.POST.get('nombre')
            if request.POST.get('costo'):
                salon.costo = request.POST.get('costo')
            if request.POST.get('ubicacion'):
                salon.ubicacion = request.POST.get('ubicacion')
            if request.POST.get('dimenLargo'):
                salon.dimenLargo = request.POST.get('dimenLargo')
            if request.POST.get('dimenAncho'):
                salon.dimenAncho = request.POST.get('dimenAncho')
            if request.POST.get('dimenAlto'):
                salon.dimenAlto = request.POST.get('dimenAlto')
            if request.POST.get('metrosCuadrados'):
                salon.metrosCuadrados = request.POST.get('metrosCuadrados')
            if request.POST.get('maxCapacidad'):
                salon.maxCapacidad = request.POST.get('maxCapacidad')
            if request.POST.get('estado_salon'):
                salon.estado_salon = models.EstadoSalon.objects.get(codigo=request.POST.get('estado_salon'))
            salon.save()
            messages.success(request, f'Salón actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return HttpResponseRedirect(reverse('salones'))