// ========================================
// VALIDAR SALONES.JS - FUNCIONAL COMPLETA
// ========================================
alert('=== INICIANDO validar-salones.js ===');

var fechaInput = document.getElementById('fecha_evento');
var salonSelect = document.getElementById('select-salon');
var montajeSelect = document.getElementById('select-montaje');
var estimadoInput = document.getElementById('estimado_asistentes');

var capacidadSalon = 0;

alert('Elementos encontrados');

// 1. Habilitar salon al cambiar fecha
if (fechaInput && salonSelect) {
    // Establecer rango de fecha (hoy + 5 meses)
    var hoy = new Date();
    var maxFecha = new Date();
    maxFecha.setMonth(hoy.getMonth() + 5);
    
    var formatoFecha = function(f) {
        var y = f.getFullYear();
        var m = String(f.getMonth() + 1).padStart(2, '0');
        var d = String(f.getDate()).padStart(2, '0');
        return y + '-' + m + '-' + d;
    };
    
    fechaInput.min = formatoFecha(hoy);
    fechaInput.max = formatoFecha(maxFecha);
    alert('Rango de fecha establecido');
    
    // Evento change
    fechaInput.onchange = function() {
        alert('Fecha seleccionada: ' + this.value);
        if (this.value) {
            salonSelect.disabled = false;
            alert('Salón habilitado');
        } else {
            salonSelect.disabled = true;
        }
    };
    alert('Evento de fecha agregado');
}

// 2. Cargar montajes al seleccionar salon
if (salonSelect && montageSelect) {
    salonSelect.onchange = function() {
        var salonId = this.value;
        alert('Salón seleccionado: ' + salonId);
        
        if (!salonId) {
            montageSelect.innerHTML = '<option value="">-- Selecciona un salón primero --</option>';
            montajeSelect.disabled = true;
            return;
        }
        
        // Obtener capacidad del salon
        var opcion = this.options[this.selectedIndex];
        capacidadSalon = parseInt(opcion.dataset.capacidad || 0);
        alert('Capacidad del salón: ' + capacidadSalon);
        
        // Cargar montajes
        cargarMontajes(salonId);
    };
}

// 3. Funcion para cargar montajes
async function cargarMontajes(salonId) {
    try {
        alert('Cargando montajes...');
        
        var response = await fetch('/reservacion/montajes-salon/?salon_id=' + salonId);
        var data = await response.json();

        alert('Montajes recibidos: ' + (data.montajes ? data.montajes.length : 0));

        // Limpiar select
        while (montajeSelect.firstChild) {
            montageSelect.removeChild(montajeSelect.firstChild);
        }

        var defaultOpt = document.createElement('option');
        defaultOpt.value = '';
        defaultOpt.textContent = '-- Selecciona un montaje --';
        montageSelect.appendChild(defaultOpt);

        if (data.montajes && data.montajes.length > 0) {
            // Filtrar montajes por capacidad del salon
            var montajesFiltrados = data.montajes.filter(function(m) {
                var cap = parseInt(m.capacidadIdeal || 0);
                return cap <= capacidadSalon;
            });

            alert('Montajes que soportan la capacidad: ' + montajesFiltrados.length);

            if (montajesFiltrados.length === 0) {
                alert('Ningún montaje soporta la capacidad del salón');
                montageSelect.disabled = true;
            } else {
                montajesFiltrados.forEach(function(m) {
                    var opt = document.createElement('option');
                    opt.value = m.tipo_montaje_id;
                    opt.textContent = m.nombre + ' (Cap: ' + (m.capacidadIdeal || 'N/A') + ')';
                    opt.dataset.capacidadIdeal = m.capacidadIdeal || 0;
                    opt.dataset.costo = m.costo || 0;
                    opt.dataset.montajeId = m.id;
                    montageSelect.appendChild(opt);
                });
                montageSelect.disabled = false;
                alert('Montajes cargados correctamente');
            }
        } else {
            alert('No hay montajes disponibles');
            montajeSelect.disabled = true;
        }
    } catch (error) {
        alert('Error: ' + error);
    }
}

// 4. Habilitar mobiliario al seleccionar montaje
if (montajeSelect) {
    montageSelect.onchange = function() {
        var opcion = this.options[this.selectedIndex];
        
        if (opcion && opcion.value) {
            var capacidadMontaje = parseInt(opcion.dataset.capacidadIdeal || 0);
            
            // Validar que la capacidad del montaje no exceda la del salon
            if (capacidadMontaje > capacidadSalon && capacidadSalon > 0) {
                alert('El montaje excede la capacidad del salón');
                this.value = '';
                deshabilitarMobiliario();
                return;
            }
            
            // Habilitar mobiliario
            var mobiliarios = document.querySelectorAll('.mobiliario-tipo');
            mobiliarios.forEach(function(s) {
                s.disabled = false;
            });
            alert('Mobiliario habilitado');
        } else {
            deshabilitarMobiliario();
        }
    };
}

function deshabilitarMobiliario() {
    var mobiliarios = document.querySelectorAll('.mobiliario-tipo');
    mobiliarios.forEach(function(s) {
        s.disabled = true;
        s.value = '';
    });
    var selects = document.querySelectorAll('.mobiliario-select');
    selects.forEach(function(s) {
        s.disabled = true;
        s.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
    });
}

// 5. Validar estimado de asistentes
if (estimadoInput && salonSelect) {
    estimadoInput.oninput = function() {
        var estimado = parseInt(this.value) || 0;
        
        if (estimado > 0 && capacidadSalon > 0 && estimado > capacidadSalon) {
            alert('El estimado excede la capacidad del salón (' + capacidadSalon + ')');
            this.value = '';
            salonSelect.value = '';
            salonSelect.disabled = true;
            montageSelect.innerHTML = '<option value="">-- Selecciona un salón primero --</option>';
            montageSelect.disabled = true;
        }
    };
}

alert('=== VALIDACION COMPLETADA ===');