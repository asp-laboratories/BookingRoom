console.log('=== INICIO validar-salones.js ===');

window.onload = function() {
    console.log('=== WINDOW ONLOAD EJECUTADO ===');

    var fechaInput = document.getElementById('fecha_evento');
    var salonSelect = document.getElementById('select-salon');
    var montagemSelect = document.getElementById('select-montaje');
    var estimadoInput = document.getElementById('estimado_asistentes');

    console.log('fechaInput:', fechaInput !== null);
    console.log('salonSelect:', salonSelect !== null);
    console.log('montagemSelect:', montagemSelect !== null);
    console.log('estimadoInput:', estimadoInput !== null);

    var capacidadSalon = 0;

    if (fechaInput && salonSelect) {
        console.log('Configurando fecha...');
        
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
        
        console.log('Fecha minima:', fechaInput.min);
        console.log('Fecha maxima:', fechaInput.max);
        
        // Usar onclick directamente para asegurar que funcione
        fechaInput.onclick = function() {
            console.log('Click en fecha detectado');
        };
        
        fechaInput.onchange = function() {
            console.log('=== CAMBIO EN FECHA ===', this.value);
            if (this.value) {
                salonSelect.disabled = false;
                console.log('SALON HABILITADO');
            } else {
                salonSelect.disabled = true;
            }
        };
        
        console.log('Eventos de fecha configurados');
    }

    if (salonSelect && montagemSelect) {
        console.log('Configurando salon change...');
        
        salonSelect.onchange = function() {
            console.log('=== CAMBIO EN SALON ===', this.value);
            
            if (!this.value) {
                montagemSelect.disabled = true;
                return;
            }
            
            var opcion = this.options[this.selectedIndex];
            capacidadSalon = parseInt(opcion.dataset.capacidad || 0);
            console.log('Capacidad salon:', capacidadSalon);
            
            // Llamar a cargar montajes
            console.log('Llamando cargarMontajes...');
            cargarMontajes(this.value);
        };
        
        console.log('Evento salon.change configurado');
    }

    function cargarMontajes(salonId) {
        console.log('=== CARGAR MONTajes ===', salonId);
        
        fetch('/reservacion/montajes-salon/?salon_id=' + salonId)
            .then(function(response) { return response.json(); })
            .then(function(data) {
                console.log('Data montajes:', data);
                console.log('Montajes length:', data.montajes ? data.montajes.length : 0);
                
                while (montagemSelect.firstChild) {
                    montagemSelect.removeChild(montagemSelect.firstChild);
                }
                
                var defaultOpt = document.createElement('option');
                defaultOpt.value = '';
                defaultOpt.textContent = '-- Selecciona un montaje --';
                montagemSelect.appendChild(defaultOpt);
                
                // Siempre habilitar el select, aunque no haya montajes
                // Así el usuario puede ver qué opciones tiene (o que no hay)
                if (data.montajes && data.montajes.length > 0) {
                    console.log('Hay', data.montajes.length, 'montajes');
                    
                    data.montajes.forEach(function(m) {
                        var opt = document.createElement('option');
                        opt.value = m.tipo_montaje_id;
                        opt.textContent = m.nombre + ' (Cap: ' + (m.capacidadIdeal || 'N/A') + ')';
                        opt.dataset.capacidadIdeal = m.capacidadIdeal || 0;
                        opt.dataset.costo = m.costo || 0;
                        opt.dataset.montajeId = m.id;
                        montagemSelect.appendChild(opt);
                    });
                } else {
                    // Agregar opción indicando que no hay montajes
                    var optNoMontaje = document.createElement('option');
                    optNoMontaje.value = '';
                    optNoMontaje.textContent = '-- No hay montajes disponibles --';
                    optNoMontaje.disabled = true;
                    montagemSelect.appendChild(optNoMontaje);
                    console.log('No hay montajes para este salón');
                }
                
                // SIEMPRE habilitar el select
                montagemSelect.disabled = false;
                console.log('=== MONTAGE SELECT HABILITADO ===');
            })
            .catch(function(error) {
                console.error('Error:', error);
                montagemSelect.disabled = false;
            });
    }

    console.log('=== FIN CONFIGURACION ===');
};

console.log('=== FIN SCRIPT ===');