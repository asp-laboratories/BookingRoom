console.log('=== INICIO validar-salones.js ===');

window.onload = function() {
    console.log('=== WINDOW ONLOAD EJECUTADO ===');

    var fechaInput = document.getElementById('fecha_evento');
    var salonSelect = document.getElementById('select-salon');
    var montagemSelect = document.getElementById('select-montaje');
    var estimadoInput = document.getElementById('estimado_asistentes');

    console.log('fechaInput:', fechaInput !== null);
    console.log('salonSelect:', salonSelect !== null);

    var capacidadSalon = 0;
    var salonesDisponibles = {};

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
        
        function verificarSalonesDisponibles(fecha) {
            console.log('=== VERIFICANDO SALONES PARA FECHA:', fecha);
            
            fetch('/reservacion/verificar-salones-disponibles/?fecha=' + fecha)
                .then(function(response) { return response.json(); })
                .then(function(data) {
                    console.log('Data disponibilidad:', data);
                    
                    if (data.success && data.salones) {
                        data.salones.forEach(function(salon) {
                            salonesDisponibles[salon.id] = salon.disponible;
                            console.log('Salon', salon.id, '-', salon.nombre, ': disponible =', salon.disponible, ', reservado =', salon.reservado, ', estado =', salon.estado_salon);
                        });
                        
                        actualizarDisponibilidadSalones();
                    }
                })
                .catch(function(error) {
                    console.error('Error verificando salones:', error);
                });
        }
        
        function actualizarDisponibilidadSalones() {
            var opciones = salonSelect.querySelectorAll('option');
            
            opciones.forEach(function(opt) {
                var salonId = parseInt(opt.value);
                
                if (salonId && salonesDisponibles[salonId] === false) {
                    opt.disabled = true;
                    opt.textContent = opt.textContent + ' (NO DISPONIBLE)';
                } else if (salonId && salonesDisponibles[salonId] === true) {
                    opt.disabled = false;
                    opt.textContent = opt.textContent.replace(' (NO DISPONIBLE)', '');
                }
            });
        }
        
        fechaInput.onchange = function() {
            console.log('=== CAMBIO EN FECHA ===', this.value);
            
            if (this.value) {
                salonSelect.disabled = false;
                console.log('SALON HABILITADO');
                verificarSalonesDisponibles(this.value);
            } else {
                salonSelect.disabled = true;
                salonesDisponibles = {};
                var opciones = salonSelect.querySelectorAll('option');
                opciones.forEach(function(opt) {
                    opt.disabled = false;
                    opt.textContent = opt.textContent.replace(' (NO DISPONIBLE)', '');
                });
                resetearMontaje();
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
            
            var salonId = parseInt(this.value);
            if (salonesDisponibles[salonId] === false) {
                alert('Este salon no esta disponible para la fecha seleccionada');
                this.value = '';
                montagemSelect.disabled = true;
                return;
            }
            
            console.log('Llamando cargarMontajes...');
            cargarMontajes(this.value);
        };
        
        console.log('Evento salon.change configurado');
    }

    function cargarMontajes(salonId) {
        console.log('=== CARGAR MONTajes ===', salonId);
        
        // Usar el endpoint de API como en Flutter: /api/tipo-montaje/?salon={salonId}
        // Este filtra los montajes cuya capacidadIdeal <= maxCapacidad del salon
        fetch('/api/tipo-montaje/?salon=' + salonId)
            .then(function(response) { return response.json(); })
            .then(function(data) {
                console.log('Data montajes:', data);
                
                while (montagemSelect.firstChild) {
                    montagemSelect.removeChild(montagemSelect.firstChild);
                }
                
                var defaultOpt = document.createElement('option');
                defaultOpt.value = '';
                defaultOpt.textContent = '-- Selecciona un montaje --';
                montagemSelect.appendChild(defaultOpt);
                
                // El API devuelve los resultados en 'results' para paginated responses
                var montajes = data.results || data;
                
                if (montajes && montajes.length > 0) {
                    console.log('Hay', montajes.length, 'montajes');
                    
                    montajes.forEach(function(m) {
                        var opt = document.createElement('option');
                        opt.value = m.id;
                        opt.textContent = m.nombre + ' (Cap: ' + (m.capacidadIdeal || 'N/A') + ')';
                        opt.dataset.capacidadIdeal = m.capacidadIdeal || 0;
                        opt.dataset.costo = m.costo || 0;
                        montagemSelect.appendChild(opt);
                    });
                } else {
                    var optNoMontaje = document.createElement('option');
                    optNoMontaje.value = '';
                    optNoMontaje.textContent = '-- No hay montajes disponibles --';
                    optNoMontaje.disabled = true;
                    montagemSelect.appendChild(optNoMontaje);
                }
                
                montagemSelect.disabled = false;
                console.log('=== MONTAGE SELECT HABILITADO ===');
            })
            .catch(function(error) {
                console.error('Error:', error);
            });
    }

    function resetearMontaje() {
        montagemSelect.innerHTML = '<option value="">-- Selecciona un montaje --</option>';
        montagemSelect.disabled = true;
        
        // Deshabilitar selects de mobiliario
        var mobiliariosTipos = document.querySelectorAll('.mobiliario-tipo');
        mobiliariosTipos.forEach(function(select) {
            select.disabled = true;
            select.value = '';
        });
    }

    // Habilitar mobiliario al seleccionar montaje
    if (montagemSelect) {
        montagemSelect.onchange = function() {
            console.log('=== CAMBIO EN MONTAJE ===', this.value);
            
            if (this.value) {
                // Habilitar todos los selects de tipo de mobiliario
                var mobiliariosTipos = document.querySelectorAll('.mobiliario-tipo');
                console.log('找到 ' + mobiliariosTipos.length + ' selects de mobiliario');
                
                mobiliariosTipos.forEach(function(select) {
                    select.disabled = false;
                    console.log('Mobiliario tipo habilitado');
                });
            } else {
                // Deshabilitar si no hay montaje seleccionado
                var mobiliariosTipos = document.querySelectorAll('.mobiliario-tipo');
                mobiliariosTipos.forEach(function(select) {
                    select.disabled = true;
                    select.value = '';
                });
            }
        };
    }

    console.log('=== FIN CONFIGURACION ===');
};

console.log('=== FIN SCRIPT ===');