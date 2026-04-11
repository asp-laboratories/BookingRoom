from django.core.management.base import BaseCommand
from datetime import date
from BookingRoomApp import models
from api.services import reservacionesService 

class Command(BaseCommand):
    help = 'Actualizacion de estados de reservaciones que ya se vencieron y las que se estan llevando hoy'

    def handle(self, *args, **kwargs):
        hoy = date.today()
        reservaciones_vencidas = models.Reservacion.objects.filter(
            fechaEvento__lt=hoy
        ).exclude(
            estado_reserva__codigo__in=['FINAL', 'CANCE', 'PAQUE']
        )

        contador_finalizadas = 0
        contador_canceladas = 0

        for reservacion in reservaciones_vencidas:
            codigo_actual = reservacion.estado_reserva.codigo
            
            try:
                if codigo_actual in ['LIQUI', 'PAGAD']:
                    reservacionesService.cambio_estado_reservacion(reservacion, 'FINAL')
                    contador_finalizadas += 1
                
                else:
                    reservacionesService.cambio_estado_reservacion(reservacion, 'CANCE')
                    contador_canceladas += 1
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error (pasadas) al modificar reservacion: {reservacion.id}: {str(e)}"))

        reservaciones_hoy = models.Reservacion.objects.filter(
            fechaEvento=hoy
        ).exclude(
            estado_reserva__codigo__in=['FINAL', 'CANCE', 'PAQUE', 'ENPRO']
        )

        contador_en_proceso = 0
        contador_canceladas_hoy = 0

        for reservacion in reservaciones_hoy:
            try:
                if reservacion.estado_reserva.codigo in ['LIQUI', 'PAGAD']:
                    reservacionesService.cambio_estado_reservacion(reservacion, 'ENPRO')
                    contador_en_proceso += 1
                else:
                    reservacionesService.cambio_estado_reservacion(reservacion, 'CANCE')
                    contador_canceladas_hoy += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error (hoy) en ID {reservacion.id}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(
            f"Cambios completados: reservaciones pasadas finalizadas: {contador_finalizadas} | Canceladas y Liberadas pasadas: {contador_canceladas}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Eventos en proceso: {contador_en_proceso} | Canceladas por falta de pago: {contador_canceladas_hoy}"
        ))