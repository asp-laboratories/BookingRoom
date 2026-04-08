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
        try {
            const response = await fetch(`/api/reservaciones-por-fecha/?fecha=${info.dateStr}`);
            const data = await response.json();
            
            const contenedorEventos = document.getElementById('contenedor-eventos');
            const contenedorResumen = document.getElementById('contenedor-resumen');
            
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            if (contenedorEventos) contenedorEventos.style.display = 'none';
            
            if (contenedorResumen) {
                contenedorResumen.style.display = 'block';
                
                if (data.reservaciones && data.reservaciones.length > 0) {
                    let html = `
                        <div class="resumen-header">
                            <h3>Reservaciones del ${info.dateStr}</h3>
                            <button class="boton-accion btn-volver" onclick="volverATabs()">← Volver</button>
                        </div>`;
                    
                    data.reservaciones.forEach(function(reservacion) {
                        html += `
                        <div class="contenedor-solicitud">
                            <span>${reservacion.nombreEvento}</span>
                            <span class="estado-badge ${reservacion.estado_codigo || ''}">${reservacion.estado_nombre || 'N/A'}</span>
                            <button class="boton-accion boton-beo ver-detalles-completo" data-pk="${reservacion.id}">
                                Ver detalles
                            </button>
                        </div>`;
                    });
                    
                    contenedorResumen.innerHTML = html;
                    
                    document.querySelectorAll('.ver-detalles-completo').forEach(btn => {
                        btn.addEventListener('click', function() {
                            const pk = this.dataset.pk;
                            if (typeof abrirModalDetalleCompleto === 'function') {
                                abrirModalDetalleCompleto(pk);
                            }
                        });
                    });
                } else {
                    contenedorResumen.innerHTML = `
                        <div class="resumen-header">
                            <h3>Reservaciones del ${info.dateStr}</h3>
                            <button class="boton-accion btn-volver" onclick="volverATabs()">← Volver</button>
                        </div>
                        <p class="sin-resultados">No hay reservaciones para el ${info.dateStr}</p>`;
                }
            }
        } catch (error) {
            console.error('Error al cargar reservaciones:', error);
            mostrarToastExito('Error al cargar reservaciones', 'error');
        }
      }
    });
    calendar.render();
    calendar.updateSize();
});
