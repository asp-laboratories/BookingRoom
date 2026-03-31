let contadorServicios = 1;
let contadorEquipamientos = 1;

function añadirSelect() {
    contadorServicios++;
    
    const contenedor = document.getElementById('servicios-selects');
    
    // Obtener tipos de servicio del primer select
    const primerSelectTipo = document.querySelector('#servicios select');
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : '';
    
    // Crear nuevo par de selects
    const nuevoPair = document.createElement('div');
    nuevoPair.className = 'servicio-pair';
    nuevoPair.setAttribute('data-index', contadorServicios);
    nuevoPair.innerHTML = `
        <div class="reservacion-campo">
            <label class="reservacion-label">Tipo de servicio</label>
            <select class="reservacion-input servicio-tipo" name="servicio_tipo_${contadorServicios}">
                ${opcionesTipo}
            </select>
        </div>
        <div class="reservacion-campo">
            <label class="reservacion-label">Seleccionar Servicio</label>
            <select class="reservacion-input servicio-select" name="servicio_${contadorServicios}" disabled>
                <option value="">-- Selecciona un tipo primero --</option>
            </select>
        </div>
    `;
    
    contenedor.appendChild(nuevoPair);
    
    // Agregar event listener al nuevo select de tipo
    const nuevoTipoSelect = nuevoPair.querySelector('.servicio-tipo');
    nuevoTipoSelect.addEventListener('change', function() {
        cargarServiciosPorTipo(this, nuevoPair.querySelector('.servicio-select'));
    });
    
    // Agregar event listener al nuevo select de servicio
    const nuevoServicioSelect = nuevoPair.querySelector('.servicio-select');
    nuevoServicioSelect.addEventListener('change', function() {
        actualizarOpcionesSelect('servicio-select');
    });
}

function añadirEquipamiento() {
    contadorEquipamientos++;
    
    const contenedor = document.getElementById('equipamientos-selects');
    const primerSelectTipo = document.querySelector('#equipamientos .reservacion-campo:first-child select');
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : '';
    
    // Crear nuevo par de selects con cantidad
    const nuevoPair = document.createElement('div');
    nuevoPair.className = 'servicio-pair';
    nuevoPair.setAttribute('data-index', contadorEquipamientos);
    nuevoPair.innerHTML = `
        <div class="reservacion-campo">
            <label class="reservacion-label">Tipo de equipamiento</label>
            <select class="reservacion-input equipamiento-tipo" name="equipamiento_tipo_${contadorEquipamientos}">
                ${opcionesTipo}
            </select>
        </div>
        <div class="reservacion-campo">
            <label class="reservacion-label">Seleccionar Equipo</label>
            <select class="reservacion-input equipamiento-select" name="equipamiento_${contadorEquipamientos}" disabled>
                <option value="">-- Selecciona un tipo primero --</option>
            </select>
        </div>
        <div class="reservacion-campo">
            <label class="reservacion-label">Cantidad</label>
            <input type="number" class="reservacion-input" name="equipamiento_cantidad_${contadorEquipamientos}" value="1" min="1" />
        </div>
    `;
    
    contenedor.appendChild(nuevoPair);
    
    // Agregar event listener al nuevo select de tipo
    const nuevoTipoSelect = nuevoPair.querySelector('.equipamiento-tipo');
    nuevoTipoSelect.addEventListener('change', function() {
        cargarEquipamientoPorTipo(this, nuevoPair.querySelector('.equipamiento-select'));
    });
    
    // Agregar event listener al nuevo select de equipamento
    const nuevoEquipamentoSelect = nuevoPair.querySelector('.equipamiento-select');
    nuevoEquipamentoSelect.addEventListener('change', function() {
        actualizarOpcionesSelect('equipamiento-select');
    });
}

function quitarSelect(tipo) {
    let contenedor;
    if (tipo === 'servicios') {
        contenedor = document.getElementById('servicios-selects');
    } else if (tipo === 'equipamientos') {
        contenedor = document.getElementById('equipamientos-selects');
    }
    
    if (contenedor) {
        const pairs = contenedor.querySelectorAll('.servicio-pair');
        if (pairs.length > 1) {
            contenedor.removeChild(pairs[pairs.length - 1]);
        } else {
            mostrarToastExito('Debe mantener al menos uno', 'warning');
        }
    }
}

// Cargar servicios por tipo
async function cargarServiciosPorTipo(tipoSelect, servicioSelect) {
    const tipoId = tipoSelect.value;
    
    if (!tipoId) {
        servicioSelect.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
        servicioSelect.disabled = true;
        return;
    }
    
    try {
        const response = await fetch(`/reservacion/servicios-por-tipo/?tipo_id=${tipoId}`);
        const data = await response.json();
        
        // Obtener servicios ya seleccionados en otros selects
        const serviciosYaSeleccionados = Array.from(document.querySelectorAll('.servicio-select'))
            .filter(s => s !== servicioSelect)
            .map(s => s.value)
            .filter(v => v !== '');
        
        servicioSelect.innerHTML = '<option value="">-- Elige un servicio --</option>';
        
        if (data.servicios && data.servicios.length > 0) {
            data.servicios.forEach(servicio => {
                const option = document.createElement('option');
                option.value = servicio.id;
                option.textContent = `${servicio.nombre} - $${servicio.costo}`;
                option.dataset.costo = servicio.costo;
                
                // Deshabilitar si ya está seleccionado en otro select
                if (serviciosYaSeleccionados.includes(String(servicio.id))) {
                    option.disabled = true;
                    option.textContent += ' (ya seleccionado)';
                }
                
                servicioSelect.appendChild(option);
            });
            servicioSelect.disabled = false;
        } else {
            servicioSelect.innerHTML = '<option value="">-- No hay servicios disponibles --</option>';
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarToastExito('Error al cargar servicios', 'error');
    }
}

// Cargar equipamiento por tipo
async function cargarEquipamientoPorTipo(tipoSelect, equipamentoSelect) {
    const tipoId = tipoSelect.value;
    
    if (!tipoId) {
        equipamentoSelect.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
        equipamentoSelect.disabled = true;
        return;
    }
    
    try {
        const response = await fetch(`/reservacion/equipamiento-por-tipo/?tipo_id=${tipoId}`);
        const data = await response.json();
        
        // Obtener equipamentos ya seleccionados en otros selects
        const equiposYaSeleccionados = Array.from(document.querySelectorAll('.equipamiento-select'))
            .filter(s => s !== equipamentoSelect)
            .map(s => s.value)
            .filter(v => v !== '');
        
        equipamentoSelect.innerHTML = '<option value="">-- Elige un equipamento --</option>';
        
        if (data.equipamientos && data.equipamientos.length > 0) {
            data.equipamientos.forEach(equip => {
                const option = document.createElement('option');
                option.value = equip.id;
                option.textContent = `${equip.nombre} - $${equip.costo} (Stock: ${equip.stock})`;
                option.dataset.costo = equip.costo;
                option.dataset.stock = equip.stock;
                
                // Deshabilitar si ya está seleccionado en otro select
                if (equiposYaSeleccionados.includes(String(equip.id))) {
                    option.disabled = true;
                    option.textContent += ' (ya seleccionado)';
                }
                
                equipamentoSelect.appendChild(option);
            });
            equipamentoSelect.disabled = false;
        } else {
            equipamentoSelect.innerHTML = '<option value="">-- No hay equipamentos disponibles --</option>';
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarToastExito('Error al carregar equipamentos', 'error');
    }
}

// Función para deshabilitar opciones seleccionadas
function actualizarOpcionesSelect(claseSelect) {
    const selects = document.querySelectorAll('.' + claseSelect);
    
    if (selects.length === 0) return;
    
    // Obtener todos los valores seleccionados actualmente
    const valoresSeleccionados = Array.from(selects)
        .map(seleccion => seleccion.value)
        .filter(valor => valor !== "");

    // Recorrer cada select y deshabilitar/habilitar opciones
    selects.forEach(function(select) {
        Array.from(select.options).forEach(function(option) {
            // Si el valor ya está seleccionado en otro select, deshabilitar
            if (valoresSeleccionados.includes(option.value) && option.value !== select.value) {
                option.disabled = true;
            } else {
                option.disabled = false;
            }
        });
    });
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Servicios - listeners para todos los selects de tipo
    document.querySelectorAll('.servicio-tipo').forEach(function(select) {
        select.addEventListener('change', function() {
            const pair = this.closest('.servicio-pair');
            const servicioSelect = pair.querySelector('.servicio-select');
            cargarServiciosPorTipo(this, servicioSelect);
        });
    });
    
    // Servicios - listeners para deshabilitar opciones repetidas
    document.querySelectorAll('.servicio-select').forEach(function(select) {
        select.addEventListener('change', function() {
            actualizarOpcionesSelect('servicio-select');
        });
    });
    
    // Equipamientos - listeners para todos los selects de tipo
    document.querySelectorAll('.equipamiento-tipo').forEach(function(select) {
        select.addEventListener('change', function() {
            const pair = this.closest('.servicio-pair');
            const equipamentoSelect = pair.querySelector('.equipamiento-select');
            cargarEquipamientoPorTipo(this, equipamentoSelect);
        });
    });
    
    // Equipamientos - listeners para deshabilitar opciones repetidas
    document.querySelectorAll('.equipamiento-select').forEach(function(select) {
        select.addEventListener('change', function() {
            actualizarOpcionesSelect('equipamiento-select');
        });
    });
});
