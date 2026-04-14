
function datosReservacion() {
    // Validar cliente
    const cliente = document.getElementById('cliente-rfc')?.value;
    const clienteNombre = document.getElementById('cliente-nombre')?.value?.trim();
    const clienteApellidoPaterno = document.getElementById('cliente-apellido-paterno')?.value?.trim();
    const clienteNombreFiscal = document.getElementById('cliente-nombre-fiscal')?.value?.trim();
    const clienteColonia = document.getElementById('cliente-colonia')?.value?.trim();
    const clienteCalle = document.getElementById('cliente-calle')?.value?.trim();
    const clienteNumero = document.getElementById('cliente-numero')?.value?.trim();
    const clienteTelefono = document.getElementById('cliente-telefono')?.value?.trim();
    const clienteCorreo = document.getElementById('cliente-correo')?.value?.trim();

    if (!cliente) {
        mostrarToastExito('Cliente no localizado. Busca o registra un cliente.', 'error');
        return null;
    }

    if (!clienteNombre) {
        mostrarToastExito('Falta el nombre del cliente', 'error');
        return null;
    }

    if (!clienteApellidoPaterno) {
        mostrarToastExito('Falta el primer apellido del cliente', 'error');
        return null;
    }

    if (!clienteNombreFiscal) {
        mostrarToastExito('Falta el nombre fiscal del cliente', 'error');
        return null;
    }

    if (!clienteColonia) {
        mostrarToastExito('Falta la colonia del cliente', 'error');
        return null;
    }

    if (!clienteCalle) {
        mostrarToastExito('Falta la calle del cliente', 'error');
        return null;
    }

    if (!clienteNumero) {
        mostrarToastExito('Falta el número del cliente', 'error');
        return null;
    }

    if (!clienteTelefono) {
        mostrarToastExito('Falta el teléfono del cliente', 'error');
        return null;
    }

    if (!clienteCorreo) {
        mostrarToastExito('Falta el correo del cliente', 'error');
        return null;
    }

    const trabajador = document.getElementById('trabajador_id').value;
    if (!trabajador) {
        mostrarToastExito("No se identifico al trabajador", "error")
        return null;
    }

    // Validar datos del evento
    const nombre = document.getElementById('nombreEvento')?.value?.trim();
    const tipo_evento = document.getElementById('tipo_evento')?.value;
    const fechaEvento = document.getElementById('fecha_evento')?.value;
    const estimaAsistentes = document.getElementById('estimado_asistentes')?.value;
    const horaInicio = document.getElementById('hora_inicio')?.value;
    const horaFin = document.getElementById('hora_fin')?.value;
    const descripEvento = document.getElementById('descripcion_evento')?.value?.trim();

    if (!nombre) {
        mostrarToastExito('Falta el nombre del evento', 'error');
        return null;
    }

    if (!tipo_evento) {
        mostrarToastExito('Falta seleccionar el tipo de evento', 'error');
        return null;
    }

    if (!fechaEvento) {
        mostrarToastExito('Falta la fecha del evento', 'error');
        return null;
    }

    if (!estimaAsistentes) {
        mostrarToastExito('Falta el número de asistentes', 'error');
        return null;
    }

    if (!horaInicio) {
        mostrarToastExito('Falta la hora de inicio', 'error');
        return null;
    }

    if (!horaFin) {
        mostrarToastExito('Falta la hora de fin', 'error');
        return null;
    }

    if (!descripEvento) {
        mostrarToastExito('Falta la descripción del evento', 'error');
        return null;
    }

    // Validar salón y montaje
    const salon = document.getElementById('select-salon')?.value;
    const selectMontaje = document.getElementById('select-montaje');
    const selectedMontajeOption = selectMontaje?.options[selectMontaje.selectedIndex];
    const tipoMontajeId = selectedMontajeOption?.dataset.tipoMontajeId;

    if (!salon) {
        mostrarToastExito('Falta seleccionar un salón', 'error');
        return null;
    }

    if (!tipoMontajeId) {
        mostrarToastExito('Falta seleccionar un montaje', 'error');
        return null;
    }

    console.log('=== Datos de Montaje para Reservación ===');
    console.log('Salón ID:', salon);
    console.log('Tipo Montaje ID:', tipoMontajeId);

    // Validar mobiliarios (al menos uno)
    const mobiliarios = [];
    let hayMobiliarioValido = false;
    
    document.querySelectorAll('.mobil-pair').forEach(pair => {
        const mobiliarioSeleccionado = pair.querySelector('.mobiliario-select');
        const cantidad = pair.querySelector('input[type="number"]');

        if (mobiliarioSeleccionado && mobiliarioSeleccionado.value && cantidad && cantidad.value) {
            mobiliarios.push({
                id: mobiliarioSeleccionado.value,
                cantidad: parseInt(cantidad.value)
            });
            hayMobiliarioValido = true;
        } else if (mobiliarioSeleccionado && mobiliarioSeleccionado.value) {
            mostrarToastExito("Datos de mobiliario incompletos", "error");
        }
    });

    if (!hayMobiliarioValido) {
        mostrarToastExito('Agrega al menos un mobiliario', 'error');
        return null;
    }

    const montaje = {
        salon: parseInt(salon),
        tipo_montaje: parseInt(tipoMontajeId),
        mobiliarios
    };

    console.log('Montaje object being sent:', montaje);

    // Servicios (OPCIONAL)
    const reserva_servicio = [];
    document.querySelectorAll('.servicio-select').forEach(pair => {
        if (pair.value) {
            reserva_servicio.push({id: parseInt(pair.value)});
        }
    });

    // Equipamiento (OPCIONAL)
    const reserva_equipa = [];
    document.querySelectorAll('.equipo-pair').forEach(pair => {
        const equipamiento = pair.querySelector('.equipamiento-select');
        const cantidad = pair.querySelector('input[type="number"]');

        if (equipamiento && cantidad && equipamiento.value && cantidad.value) {
            reserva_equipa.push({
                id: parseInt(equipamiento.value),
                cantidad: parseInt(cantidad.value)
            })
        }

    });

    // Determinar el estado según la página
    // Si estamos en la página de cliente, enviar como SOLIC (solicitud)
    // Si estamos en la página de recepción, enviar como PEN (pendiente)
    const esPaginaCliente = window.location.pathname.includes('cliente');
    const estadoReserva = esPaginaCliente ? 'SOLIC' : 'PEN';

    return {
        nombre: nombre,
        descripEvento: descripEvento,
        estimaAsistentes: parseInt(estimaAsistentes),
        fechaEvento: fechaEvento,
        horaInicio: horaInicio,
        horaFin: horaFin,
        cliente: cliente,
        trabajador: trabajador,
        estado_reserva: estadoReserva,  // SOLIC para cliente, PEN para recepción
        reserva_servicio: reserva_servicio,
        reserva_equipa: reserva_equipa,
        montaje: montaje,
        tipo_evento: parseInt(tipo_evento)
    };
}

function obtenerError(info) {
    console.error('🔍 Respuesta de error del servidor:', JSON.stringify(info, null, 2));
    
    if (info.error) return info.error;
    if (info.message) return info.message;
    if (typeof info === 'object') {
        for (const key in info) {
            const val = info[key];
            if (Array.isArray(val)) return `${key}: ${val.join(', ')}`;
            if (typeof val === 'string') return `${key}: ${val}`;
            if (typeof val === 'object' && val !== null) {
                // Buscar errores anidados
                for (const subKey in val) {
                    const subVal = val[subKey];
                    if (Array.isArray(subVal)) return `${key}.${subKey}: ${subVal.join(', ')}`;
                    if (typeof subVal === 'string') return `${key}.${subKey}: ${subVal}`;
                }
            }
        }
    }
    return 'Error desconocido. Revisa la consola (F12) para más detalles.';
}

async function crearReservacion() {
    const datos = datosReservacion();
    if (!datos) return false;

    try {
        const respuesta = await fetch('/api/reservacion/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(datos)
        });

        const data = await respuesta.json();

        if (respuesta.ok) {
            return { success: true, id: data.id, data: data };
        } else {
            const error = obtenerError(data);
            mostrarToastExito(`Error: ${error}`, 'error')
            console.error('Error API:', data)
            return { success: false };
        }

    } catch (error) {
        mostrarToastExito("Error en la conexion con el servidor", 'error');
        console.error(error)
        return { success: false };
    }
}

let reservacionCreadaId = null;
let reservacionEnProceso = false;

async function confirmarReservacion() {
    // Prevenir doble envío
    if (reservacionEnProceso) {
        console.log('Reservación ya en proceso, ignorando clic adicional');
        return;
    }

    reservacionEnProceso = true;
    
    // Deshabilitar botón para evitar múltiples clics
    const botonConfirmar = document.querySelector('.reservacion-btn-confirmar');
    if (botonConfirmar) {
        botonConfirmar.disabled = true;
        botonConfirmar.style.opacity = '0.5';
        botonConfirmar.style.cursor = 'not-allowed';
        botonConfirmar.textContent = 'Procesando...';
    }

    // Detectar si es página de cliente
    const esPaginaCliente = window.location.pathname.includes('cliente');

    try {
        const resultado = await crearReservacion();

        if (resultado && resultado.success) {
            reservacionCreadaId = resultado.id;
            
            if (esPaginaCliente) {
                // Para clientes: mostrar éxito y redirigir a la página de cliente
                mostrarToastExito(`¡Solicitud #${resultado.id} enviada exitosamente! Un recepcionista la revisará pronto.`, 'success');
                
                setTimeout(() => {
                    window.location.href = '/cliente/reservacion/';
                }, 3000);
            } else {
                // Para recepción: preguntar si desea realizar pago
                mostrarToastExito(`¡Reservación #${resultado.id} creada exitosamente!`, 'success');
                
                setTimeout(() => {
                    abrirModalConfirmar(
                        'Reservación creada',
                        `La reservación #${resultado.id} se creó exitosamente. ¿Deseas realizar un pago ahora?`,
                        function() {
                            abrirModalPagosConReservacion(reservacionCreadaId);
                        }
                    );
                }, 500);
            }
        } else {
            // Si falló, re-habilitar el botón
            if (botonConfirmar) {
                botonConfirmar.disabled = false;
                botonConfirmar.style.opacity = '';
                botonConfirmar.style.cursor = '';
                botonConfirmar.textContent = esPaginaCliente ? 'Enviar Solicitud' : 'Confirmar';
            }
        }
    } finally {
        reservacionEnProceso = false;
    }
}

function abrirModalPagosConReservacion(reservacionId) {
    const modal = document.getElementById('modalPagos');
    if (modal) {
        const inputReservacion = modal.querySelector('[data-field="reservacion"]');
        const inputReservacionId = modal.querySelector('[data-field="reservacion_id"]');

        if (inputReservacion) inputReservacion.value = reservacionId;
        if (inputReservacionId) inputReservacionId.value = reservacionId;

        modal.showModal();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const botonReservacion = document.querySelector('.reservacion-btn-confirmar');
    if (botonReservacion) {
        botonReservacion.onclick = function () {
            abrirModalConfirmar(
                'Confirmar reservación',
                '¿Estás seguro de que deseas crear esta reservación?',
                confirmarReservacion
            );
        };
    }
});