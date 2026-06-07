document.addEventListener("DOMContentLoaded", function () {
    const inputFecha = document.getElementById('buscar-fecha-input');
    const btnBuscar = document.getElementById('btn-buscar-fecha');
    const contenedorEventos = document.getElementById('contenedor-eventos');
    const contenedorResumen = document.getElementById('contenedor-resumen');
    const tabsContainer = document.querySelector('.div2');

    let tabActivaOriginal = 'tab1';

    if (!inputFecha || !btnBuscar) {
        console.error('No se encontraron los elementos necesarios');
        return;
    }

    function ocultarTabs() {
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
    }

    function restaurarTabs() {
        const tabActiva = document.getElementById(tabActivaOriginal);
        const btnActivo = document.querySelector(`[onclick*="${tabActivaOriginal}"]`);
        
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        if (tabActiva) {
            tabActiva.classList.add('active');
        }
        
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        if (btnActivo) {
            btnActivo.classList.add('active');
        }
    }

    btnBuscar.addEventListener('click', async function () {
        const fecha = inputFecha.value;
        
        if (!fecha) {
            mostrarToastExito('Por favor selecciona una fecha', 'warning');
            return;
        }

        tabActivaOriginal = document.querySelector('.tab-btn.active')?.getAttribute('onclick')?.match(/'([^']+)'/)?.[1] || 'tab1';

        try {
            const response = await fetch(`/api/reservaciones-por-fecha/?fecha=${fecha}`);
            const data = await response.json();

            ocultarTabs();
            
            if (contenedorEventos) contenedorEventos.style.display = 'none';
            
            if (contenedorResumen) {
                contenedorResumen.style.display = 'block';
                
                if (data.reservaciones && data.reservaciones.length > 0) {
                    let html = `
                        <div class="resumen-header">
                            <h3>Reservaciones del ${fecha}</h3>
                            <button class="boton-accion btn-volver" onclick="volverATabs()">← Volver</button>
                        </div>`;
                    
                    data.reservaciones.forEach(function (reservacion) {
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
                            <h3>Reservaciones del ${fecha}</h3>
                            <button class="boton-accion btn-volver" onclick="volverATabs()">← Volver</button>
                        </div>
                        <p class="sin-resultados">No hay reservaciones para el ${fecha}</p>`;
                }
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarToastExito('Error al buscar reservaciones', 'error');
        }
    });
});

window.volverATabs = function() {
    const contenedorEventos = document.getElementById('contenedor-eventos');
    const contenedorResumen = document.getElementById('contenedor-resumen');
    
    if (contenedorEventos) contenedorEventos.style.display = 'block';
    if (contenedorResumen) {
        contenedorResumen.style.display = 'none';
        contenedorResumen.innerHTML = '';
    }
    
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    const tab1 = document.getElementById('tab1');
    if (tab1) tab1.classList.add('active');
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelector('.tab-confirm')?.classList.add('active');
};
