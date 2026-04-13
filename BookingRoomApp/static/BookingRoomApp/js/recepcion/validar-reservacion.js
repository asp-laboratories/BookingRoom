// Validaciones para la sección "Acerca de la reservación"

document.addEventListener("DOMContentLoaded", function() {
    const nombreEvento = document.getElementById('nombreEvento');
    const tipoEvento = document.getElementById('tipo_evento');
    const fechaEvento = document.getElementById('fecha_evento');
    const estimaAsistentes = document.getElementById('estimado_asistentes');
    const horaInicio = document.getElementById('hora_inicio');
    const horaFin = document.getElementById('hora_fin');
    const descripcionEvento = document.getElementById('descripcion_evento');

    // ==========================================
    // CONFIGURAR FECHA MÍNIMA (HOY)
    // ==========================================
    
    function obtenerFechaHoy() {
        const hoy = new Date();
        const year = hoy.getFullYear();
        const month = String(hoy.getMonth() + 1).padStart(2, '0');
        const day = String(hoy.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    }

    // Establecer fecha mínima en el date picker
    if (fechaEvento) {
        const fechaHoy = obtenerFechaHoy();
        fechaEvento.min = fechaHoy; // Esto deshabilita fechas anteriores en el popup
        
        // Validar al cambiar la fecha
        fechaEvento.addEventListener('change', function() {
            const fechaSeleccionada = new Date(this.value + 'T00:00:00');
            const hoy = new Date();
            hoy.setHours(0, 0, 0, 0);
            
            if (fechaSeleccionada < hoy) {
                mostrarToastExito('La fecha del evento no puede ser anterior a hoy', 'warning');
                this.value = '';
            }
        });
    }

    // ==========================================
    // VALIDACIÓN DE HORAS
    // ==========================================
    
    function validarHoras() {
        if (!horaInicio.value || !horaFin.value) return true;
        
        const inicio = horaInicio.value;
        const fin = horaFin.value;
        
        // Convertir a minutos para comparar
        const [inicioHora, inicioMin] = inicio.split(':').map(Number);
        const [finHora, finMin] = fin.split(':').map(Number);
        
        const inicioMinutos = inicioHora * 60 + inicioMin;
        const finMinutos = finHora * 60 + finMin;
        
        if (inicioMinutos >= finMinutos) {
            return false;
        }
        
        return true;
    }

    // Validar cuando cambian las horas
    if (horaInicio) {
        horaInicio.addEventListener('change', function() {
            if (!validarHoras()) {
                mostrarToastExito('La hora de inicio debe ser anterior a la hora de fin', 'warning');
                this.value = '';
                horaFin.value = '';
            }
        });
    }

    if (horaFin) {
        horaFin.addEventListener('change', function() {
            if (!validarHoras()) {
                mostrarToastExito('La hora de fin debe ser posterior a la hora de inicio', 'warning');
                this.value = '';
            }
        });
    }

    // ==========================================
    // ESTIMADO DE ASISTENTES
    // ==========================================
    
    if (estimaAsistentes) {
        estimaAsistentes.addEventListener('input', function() {
            // Solo permitir números positivos
            if (this.value < 0) {
                this.value = 0;
            }
            
            // Eliminar decimales
            this.value = this.value.replace(/[^0-9]/g, '');
        });

        estimaAsistentes.addEventListener('blur', function() {
            if (this.value && parseInt(this.value) === 0) {
                mostrarToastExito('El estimado de asistentes debe ser mayor a 0', 'warning');
            }
        });
    }

    // ==========================================
    // NOMBRE DEL EVENTO
    // ==========================================
    
    if (nombreEvento) {
        nombreEvento.addEventListener('blur', function() {
            this.value = this.value.trim();
            
            if (this.value && this.value.length < 3) {
                mostrarToastExito('El nombre del evento debe tener al menos 3 caracteres', 'warning');
            }
        });
    }

    // ==========================================
    // DESCRIPCIÓN DEL EVENTO
    // ==========================================
    
    if (descripcionEvento) {
        descripcionEvento.addEventListener('blur', function() {
            this.value = this.value.trim();
            
            if (this.value && this.value.length < 10) {
                mostrarToastExito('La descripción debe tener al menos 10 caracteres', 'warning');
            }
        });
    }

    // ==========================================
    // VALIDACIÓN COMPLETA AL CONFIRMAR
    // ==========================================
    
    const btnConfirmar = document.getElementById('btn-confirmar-reservacion');
    
    if (btnConfirmar) {
        btnConfirmar.addEventListener('click', function(e) {
            let errores = [];
            
            // Validar nombre del evento
            if (!nombreEvento.value || nombreEvento.value.trim() === '') {
                errores.push('El nombre del evento es obligatorio');
            } else if (nombreEvento.value.trim().length < 3) {
                errores.push('El nombre del evento debe tener al menos 3 caracteres');
            }
            
            // Validar tipo de evento
            if (!tipoEvento.value) {
                errores.push('Debes seleccionar un tipo de evento');
            }
            
            // Validar fecha del evento
            if (!fechaEvento.value) {
                errores.push('La fecha del evento es obligatoria');
            } else {
                const fechaSeleccionada = new Date(fechaEvento.value + 'T00:00:00');
                const hoy = new Date();
                hoy.setHours(0, 0, 0, 0);
                
                if (fechaSeleccionada < hoy) {
                    errores.push('La fecha del evento no puede ser anterior a hoy');
                }
            }
            
            // Validar estimado de asistentes
            if (!estimaAsistentes.value || parseInt(estimaAsistentes.value) === 0) {
                errores.push('El estimado de asistentes debe ser mayor a 0');
            }
            
            // Validar hora de inicio
            if (!horaInicio.value) {
                errores.push('La hora de inicio del evento es obligatoria');
            }
            
            // Validar hora de fin
            if (!horaFin.value) {
                errores.push('La hora de fin del evento es obligatoria');
            }
            
            // Validar que hora inicio < hora fin
            if (horaInicio.value && horaFin.value && !validarHoras()) {
                errores.push('La hora de inicio debe ser anterior a la hora de fin');
            }
            
            // Validar descripción
            if (!descripcionEvento.value || descripcionEvento.value.trim() === '') {
                errores.push('La descripción del evento es obligatoria');
            } else if (descripcionEvento.value.trim().length < 10) {
                errores.push('La descripción debe tener al menos 10 caracteres');
            }
            
            // Mostrar errores si los hay
            if (errores.length > 0) {
                e.preventDefault();
                e.stopImmediatePropagation();
                mostrarToastExito('Errores en la reservación:\n\n• ' + errores.join('\n• '), 'error');
                return false;
            }
            
            // Si todo está válido, continuar
            return true;
        }, true); // Capturing phase
    }
});
