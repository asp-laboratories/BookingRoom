
document.addEventListener("DOMContentLoaded", function () {
    const inputFecha = document.querySelector('.buscar-fecha');
    const btnBuscar = document.getElementById('buscar-manual-fechas');
    const contenedorEventos = document.getElementById('contenedor-eventos');
    const contenedorResumen = document.getElementById('contenedor-resumen');

    if (!inputFecha || !btnBuscar || !contenedorEventos || !contenedorResumen) {
        console.error('No se encontraron los elementos necesarios');
        return;
    }

    btnBuscar.addEventListener('click', async function () {
        const fecha = inputFecha.value;
        
        if (!fecha) {
            alert('Por favor selecciona una fecha');
            return;
        }

        try {
            const response = await fetch(`/api/reservaciones-por-fecha/?fecha=${fecha}`);
            const data = await response.json();

            if (data.reservaciones && data.reservaciones.length > 0) {
                contenedorEventos.style.display = 'none';
                contenedorResumen.style.display = 'block';
                contenedorResumen.innerHTML = '<h3>Reservaciones del ' + fecha + '</h3>';

                data.reservaciones.forEach(function (reservacion) {
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
                contenedorResumen.innerHTML = '<p>No hay reservaciones para el ' + fecha + '</p>';
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error al buscar reservaciones');
        }
    });
});