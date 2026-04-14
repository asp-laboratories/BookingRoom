// Validación de disponibilidad de salones según la fecha del evento
// Inspirado en la lógica de FollowRoom Flutter (tab_salon_reservacion.dart)

document.addEventListener("DOMContentLoaded", function() {
    const fechaEventoInput = document.getElementById('fecha_evento');
    const selectSalon = document.getElementById('select-salon');
    const selectMontaje = document.getElementById('select-montaje');
    const mobiliarioTipoSelects = document.querySelectorAll('.mobiliario-tipo');

    // Estados que bloquean un salón (según Flutter: tab_salon_reservacion.dart)
    const estadosBloqueados = ['Ocupado', 'Reservado', 'En Limpieza', 'Mantenimiento'];

    // Cuando cambia la fecha del evento, verificar disponibilidad de salones
    if (fechaEventoInput) {
        fechaEventoInput.addEventListener('change', async function() {
            const fecha = this.value;
            
            // Resetear selección de salon, montaje y mobiliario al cambiar fecha
            selectSalon.value = '';
            selectMontaje.innerHTML = '<option value="">-- Selecciona un salón primero --</option>';
            selectMontaje.disabled = true;
            mobiliarioTipoSelects.forEach(s => {
                s.disabled = true;
                s.value = '';
            });
            document.querySelectorAll('.mobiliario-select').forEach(s => {
                s.disabled = true;
                s.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
            });
            
            if (!fecha) {
                // Sin fecha, deshabilitar salon
                selectSalon.disabled = true;
                return;
            }

            console.log('=== Verificando salones para fecha:', fecha, '===');
            
            // Habilitar el select de salon mientras se verifica
            selectSalon.disabled = false;
            
            // Verificar disponibilidad de salones
            await verificarDisponibilidadSalones(fecha);
        });
    }

    // Función para verificar la disponibilidad de salones en una fecha específica
    async function verificarDisponibilidadSalones(fecha) {
        try {
            const response = await fetch(`/reservacion/verificar-salones-disponibles/?fecha=${fecha}`);
            const data = await response.json();

            if (!data.success) {
                console.error('Error al verificar salones:', data.message);
                return;
            }

            // data.salones contiene: { id, nombre, disponible, estado_salon, reservado }
            const opcionesSalon = selectSalon.querySelectorAll('option');

            opcionesSalon.forEach(opcion => {
                const salonId = opcion.value;
                if (!salonId) return; // Skip the default option

                const salonInfo = data.salones.find(s => s.id == salonId);

                if (salonInfo) {
                    const estaBloqueado = salonInfo.reservado ||
                        estadosBloqueados.includes(salonInfo.estado_salon);

                    if (estaBloqueado) {
                        opcion.disabled = true;
                        opcion.textContent = `${salonInfo.nombre} (Cap: ${salonInfo.max_capacidad || '?'}) [No disponible]`;
                    } else {
                        opcion.disabled = false;
                        // Mantener la capacidad en el texto
                        opcion.textContent = `${salonInfo.nombre} (Cap: ${salonInfo.max_capacidad || '?'})`;
                    }
                }
            });

            console.log('Salones verificados:', data.salones);

        } catch (error) {
            console.error('Error al verificar disponibilidad de salones:', error);
        }
    }

    // Cuando se selecciona un salón, habilitar montaje y cargar montajes
    if (selectSalon) {
        selectSalon.addEventListener('change', function() {
            const salonSeleccionado = this.value;

            if (!salonSeleccionado) {
                // Deshabilitar montaje y mobiliario si no hay salón seleccionado
                selectMontaje.disabled = true;
                selectMontaje.innerHTML = '<option value="">-- Selecciona un salón primero --</option>';
                mobiliarioTipoSelects.forEach(s => {
                    s.disabled = true;
                    s.value = '';
                });
                return;
            }

            // Verificar si el salón está disponible (no está disabled)
            const opcionSeleccionada = this.options[this.selectedIndex];
            if (opcionSeleccionada.disabled) {
                mostrarToastExito('Este salón no está disponible para la fecha seleccionada', 'warning');
                this.value = '';
                return;
            }

            // Cargar montajes del salón seleccionado
            if (typeof cargarMontajesSalon === 'function') {
                cargarMontajesSalon(salonSeleccionado);
            }

            console.log('Salón seleccionado:', salonSeleccionado);
        });
    }

    // Cuando se selecciona un montaje, habilitar mobiliario
    if (selectMontaje) {
        selectMontaje.addEventListener('change', function() {
            const montajeSeleccionado = this.value;
            if (montajeSeleccionado) {
                mobiliarioTipoSelects.forEach(s => {
                    s.disabled = false;
                });
            } else {
                mobiliarioTipoSelects.forEach(s => {
                    s.disabled = true;
                    s.value = '';
                });
            }
        });
    }
});
