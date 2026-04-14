// Validación de salones, montaje y capacidad
// Basado en la lógica de FollowRoom Flutter (tab_salon_reservacion.dart)

document.addEventListener("DOMContentLoaded", function() {
    const fechaEventoInput = document.getElementById('fecha_evento');
    const selectSalon = document.getElementById('select-salon');
    const selectMontaje = document.getElementById('select-montaje');
    const estimadoInput = document.getElementById('estimado_asistentes');

    // Estados que bloquean un salón ( Flutter: _estaBloqueado() )
    const estadosBloqueados = ['RESV', 'OCUP', 'LIMPI', 'LIMP', 'MANTE', 'MAN'];

    // Flag para evitar llamadas duplicadas
    let cargandoMontajes = false;

    // ========================================
    // 1. CAMBIO DE FECHA → Verificar salones
    // ========================================
    if (fechaEventoInput) {
        fechaEventoInput.addEventListener('change', async function() {
            const fecha = this.value;

            // Resetear todo al cambiar fecha
            selectSalon.value = '';
            selectSalon.disabled = true;
            selectMontaje.innerHTML = '<option value="">-- Selecciona un salón primero --</option>';
            selectMontaje.disabled = true;
            document.querySelectorAll('.mobiliario-tipo').forEach(s => { s.disabled = true; s.value = ''; });
            document.querySelectorAll('.mobiliario-select').forEach(s => { s.disabled = true; s.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>'; });

            if (!fecha) return;

            console.log('📅 Verificando salones para:', fecha);
            selectSalon.disabled = false;
            await verificarDisponibilidadSalones(fecha);
        });
    }

    // ========================================
    // 2. VERIFICAR DISPONIBILIDAD DE SALONES
    // ========================================
    async function verificarDisponibilidadSalones(fecha) {
        try {
            const response = await fetch(`/reservacion/verificar-salones-disponibles/?fecha=${fecha}`);
            const data = await response.json();

            if (!data.success) {
                console.error('Error verificando salones:', data.message);
                return;
            }

            // data.salones = [{ id, nombre, disponible, estado_salon, reservado, max_capacidad }]
            const opciones = selectSalon.querySelectorAll('option');

            opciones.forEach(opcion => {
                const salonId = opcion.value;
                if (!salonId) return;

                const salonInfo = data.salones.find(s => s.nombre == salonId);
                
                if (salonInfo) {
                    const estaBloqueado = salonInfo.reservado || 
                        estadosBloqueados.includes(salonInfo.estado_salon);
                    
                    if (estaBloqueado) {
                        opcion.disabled = true;
                        opcion.textContent = `${salonInfo.nombre} (No disponible - ${salonInfo.estado_salon})`;
                    } else {
                        opcion.disabled = false;
                        opcion.textContent = salonInfo.nombre;
                    }
                }
            });

            console.log('✅ Salones verificados:', data.salones.length);

        } catch (error) {
            console.error('Error verificando salones:', error);
        }
    }

    // ========================================
    // 3. SELECCIÓN DE SALÓN → Cargar montajes
    // ========================================
    if (selectSalon) {
        selectSalon.addEventListener('change', function() {
            const salonId = this.value;

            // Resetear montaje (limpieza completa)
            selectMontaje.value = '';
            while (selectMontaje.firstChild) {
                selectMontaje.removeChild(selectMontaje.firstChild);
            }
            const defaultOpt = document.createElement('option');
            defaultOpt.value = '';
            defaultOpt.textContent = '-- Selecciona un montaje --';
            selectMontaje.appendChild(defaultOpt);
            selectMontaje.disabled = true;

            // Resetear mobiliario
            document.querySelectorAll('.mobiliario-tipo').forEach(s => { s.disabled = true; s.value = ''; });
            document.querySelectorAll('.mobiliario-select').forEach(s => { s.disabled = true; s.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>'; });

            if (!salonId) return;

            // Validar que no esté bloqueado
            const opcionSeleccionada = this.options[this.selectedIndex];
            if (opcionSeleccionada.disabled) {
                mostrarToastExito('Este salón no está disponible para la fecha seleccionada', 'warning');
                this.value = '';
                return;
            }

            // Validar capacidad vs estimado
            const estimado = parseInt(estimadoInput?.value) || 0;
            const capacidadMax = parseInt(this.dataset.capacidad || opcionSeleccionada.dataset.capacidad || 0);

            if (estimado > 0 && capacidadMax > 0 && estimado > capacidadMax) {
                mostrarToastExito(
                    `⚠️ El salón tiene capacidad máxima de ${capacidadMax} personas. Tu estimado es de ${estimado} asistentes.`,
                    'warning'
                );
                this.value = '';
                return;
            }

            // Cargar montajes
            cargarMontajesSalon(salonId);
            console.log('🏛️ Salón seleccionado:', salonId);
        });
    }

    // ========================================
    // 4. VALIDAR CAPACIDAD AL CAMBIAR ESTIMADO
    // ========================================
    if (estimadoInput) {
        estimadoInput.addEventListener('change', function() {
            const estimado = parseInt(this.value) || 0;
            if (!selectSalon.value) return;

            const opcionSeleccionada = selectSalon.options[selectSalon.selectedIndex];
            const capacidadMax = parseInt(opcionSeleccionada.dataset.capacidad || 0);

            if (estimado > capacidadMax && capacidadMax > 0) {
                mostrarToastExito(
                    `⚠️ El salón tiene capacidad de ${capacidadMax} personas.`,
                    'warning'
                );
                selectSalon.value = '';
                selectMontaje.value = '';
                while (selectMontaje.firstChild) {
                    selectMontaje.removeChild(selectMontaje.firstChild);
                }
                const opt = document.createElement('option');
                opt.value = '';
                opt.textContent = '-- Selecciona un salón primero --';
                selectMontaje.appendChild(opt);
                selectMontaje.disabled = true;
            }
        });
    }

    // ========================================
    // 5. CARGAR TODOS LOS MONTAJES (como Flutter)
    // ========================================
    async function cargarMontajesSalon(salonId) {
        // Prevenir llamadas duplicadas
        if (cargandoMontajes) {
            console.log('⚠️ Ya se están cargando montajes, ignorando llamada duplicada');
            return;
        }

        cargandoMontajes = true;

        try {
            // Flutter muestra TODOS los montajes, no solo los del salón
            const response = await fetch(`/reservacion/montajes-salon/?todos=true`);
            const data = await response.json();

            // LIMPIAR completamente antes de agregar
            while (selectMontaje.firstChild) {
                selectMontaje.removeChild(selectMontaje.firstChild);
            }

            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '-- Selecciona un montaje --';
            selectMontaje.appendChild(defaultOption);

            selectMontaje.disabled = false;

            if (data.montajes && data.montajes.length > 0) {
                data.montajes.forEach(montaje => {
                    const option = document.createElement('option');
                    option.value = montaje.id;
                    option.textContent = `${montaje.nombre} (Capacidad ideal: ${montaje.capacidadIdeal || 'N/A'})`;
                    option.dataset.costo = montaje.costo || 0;
                    option.dataset.montajeId = montaje.id;
                    option.dataset.tipoMontajeId = montaje.tipo_montaje_id;
                    selectMontaje.appendChild(option);
                });
                console.log('🎨 Todos los montajes cargados:', data.montajes.length);
            } else {
                selectMontaje.innerHTML = '<option value="">-- No hay montajes disponibles --</option>';
                selectMontaje.disabled = true;
            }

        } catch (error) {
            console.error('Error cargando montajes:', error);
            mostrarToastExito('Error al cargar montajes', 'error');
        } finally {
            cargandoMontajes = false;
        }
    }

    // ========================================
    // 6. SELECCIÓN DE MONTAJE → Habilitar mobiliario
    // ========================================
    if (selectMontaje) {
        selectMontaje.addEventListener('change', function() {
            const montajeSeleccionado = this.value;
            const mobiliarioTipos = document.querySelectorAll('.mobiliario-tipo');

            if (montajeSeleccionado) {
                // Habilitar tipos de mobiliario
                mobiliarioTipos.forEach(s => s.disabled = false);
                console.log('🪑 Montaje seleccionado, mobiliario habilitado');
            } else {
                // Resetear todo el mobiliario
                mobiliarioTipos.forEach(s => { s.disabled = true; s.value = ''; });
                document.querySelectorAll('.mobiliario-select').forEach(s => {
                    s.disabled = true;
                    s.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
                });
            }
        });
    }
});
