from django.db import transaction
from django.core.exceptions import ValidationError
from BookingRoomApp import models

class Validador:
    ## Constructor
    def __init__(self, salon, fecha):
        self.salon_id = salon
        self.fecha = fecha

    def inspeccion_completa(self):
        self._validar_salon()
        self._validar_horario()
        self._validar_estado()

    def _validar_salon(self):
        if not models.Salon.objects.filter(id=self.salon_id).exists():
            raise ValidationError("El salon no existe")
    
    def _validar_horario(self):
        horario_cruzado = models.Reservacion.objects.filter(
            montaje__salon_id=self.salon_id,
            fechaEvento=self.fecha,
        )
        if horario_cruzado.exists():
            raise ValidationError("Ese dia, ese salon ya esta ocupado")
        
    def _validar_estado(self):
        salon = models.Salon.objects.get(id=self.salon_id)
        if salon.estado_salon != 'DISPO':
            raise ValidationError("El salon no se encuentra disponible")
        
class Precios:
    # Constructor
    def __init__(self, mobiliarios, equipamientos = None, servicios = None,  salon = None):
        self.servicios = servicios
        self.mobiliarios = mobiliarios
        self.salon = salon
        self.equipamientos = equipamientos
    
    def sumar_todo(self):
        total = 0
        total += self.sumar_montaje()
        if not len(self.servicios) == 0:
            total += self._sumar_servicios()
        if not len(self.equipamientos) == 0:
            total += self._sumar_equipamientos()
        return total
    
    def sumar_montaje(self):
        total = 0
        total += self._sumar_salon()
        total += self._sumar_mobiliarios()
        return total
    
    def _sumar_servicios(self):
        total = 0
        for servicio in self.servicios:
            ser = models.Servicio.objects.get(id=servicio['id'])
            total += ser.costo
        return total

    def _sumar_equipamientos(self):
        total = 0
        for equipo in self.equipamientos:
            equipamiento = models.Equipamiento.objects.get(id=equipo['id'])
            total += equipamiento.costo * equipo['cantidad']
        return total

    def _sumar_mobiliarios(self):
        total = 0
        for mobiliaio in self.mobiliarios:
            mobiliario = models.Mobiliario.objects.get(id=mobiliaio['id'])
            total += mobiliario.costo * mobiliaio['cantidad']
        return total

    def _sumar_salon(self):
        salon = models.Salon.objects.get(id=self.salon)
        return salon.costo