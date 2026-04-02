document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      locale: 'es',
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      eventColor: '#9c5c31',
      events: '/api/calendario-eventos/',
      eventBackgroundColor: '#9c5c31',
      eventBorderColor: '#9c5c31',
      eventTextColor: '#ffffff',
      dateClick: async function(info) {
        const response = await fetch(`/api/reservaciones-por-fecha/?fecha=${info.dateStr}`);
        const data = await response.json();
        
        const contenedorEventos = document.getElementById('contenedor-eventos');
        const contenedorResumen = document.getElementById('contenedor-resumen');
        
        if (!contenedorEventos || !contenedorResumen) {
            console.error('No se encontraron los contenedores');
            return;
        }
        
        if (data.reservaciones && data.reservaciones.length > 0) {
            contenedorEventos.style.display = 'none';
            contenedorResumen.style.display = 'block';
            contenedorResumen.innerHTML = '<h3>Reservaciones del ' + info.dateStr + '</h3>';
            
            data.reservaciones.forEach(function(reservacion) {
                contenedorResumen.innerHTML += `
                <div class="contenedor-solicitud">
                    <span>${reservacion.nombreEvento}</span>
                    <span>${reservacion.cliente_nombre}</span>
                    <span>${reservacion.horaInicio} - ${reservacion.horaFin}</span>
                    <button class="boton-accion boton-beo ver-detalles" data-pk="${reservacion.id}">
                        Ver detalles
                    </button>
                </div>`;
            });
        } else {
            contenedorEventos.style.display = 'none';
            contenedorResumen.style.display = 'block';
            contenedorResumen.innerHTML = '<p>No hay reservaciones para el ' + info.dateStr + '</p>';
        }
      }
    });
    calendar.render();
    calendar.updateSize();
  });