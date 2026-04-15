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
        
        fetch('/reservacion/montajes-salon/?salon_id=' + salonId)
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
    }

    console.log('=== FIN CONFIGURACION ===');
};

console.log('=== FIN SCRIPT ===');