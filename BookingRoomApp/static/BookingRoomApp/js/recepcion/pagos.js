function getPagosContainer() {
    return document.getElementById('modalPagos') || document.querySelector('.pagos-container');
}

function queryField(selector) {
    const container = getPagosContainer();
    return container ? container.querySelector(`[data-field="${selector}"]`) : null;
}

async function buscarReservacion() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const numero = document.querySelector('[data-field="reservacion"]')?.value;
    
    if (!numero) {
        alert('Ingrese el número de reservación');
        return;
    }

    try {
        const respuesta = await fetch(`/api/buscar-reservacion/?numero=${numero}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken || ''
            },
            credentials: 'same-origin'
        });

        if (respuesta.ok) {
            const datos = await respuesta.json();

            // Validar que la reservación no esté en estado "Solicitada"
            if (datos.estado && datos.estado.toLowerCase().includes('solicitada')) {
                alert('La reservación está en estado "Solicitada". Debe ser aceptada primero antes de realizar pagos.');
                limpiarCampos();
                return;
            }

            document.querySelector('[data-field="cliente"]').value = datos.cliente || '';
            document.querySelector('[data-field="nombre_evento"]').value = datos.nombre_evento || '';
            document.querySelector('[data-field="descripcion"]').value = datos.descripcion || '';
            document.querySelector('[data-field="subtotal"]').value = datos.subtotal || '';
            document.querySelector('[data-field="total"]').value = datos.total || '';
            document.querySelector('[data-field="saldo"]').value = datos.saldo_restante || '';
            document.querySelector('[data-field="reservacion_id"]').value = datos.id || '';
            document.querySelector('[data-field="estado"]').value = datos.estado || '';
            
            const saldo = parseFloat(datos.saldo_restante) || 0;
            let montoSugerido = saldo;
            
            if (datos.pagos_count === 0) {
                montoSugerido = Math.ceil(saldo / 2);
            }
            
            document.querySelector('[data-field="monto"]').value = montoSugerido.toFixed(2);

            if(saldo==0){
                document.querySelector('[data-field="saldo"]').value = "El pago esta compleado";
            }




            
        } else {
            const error = await respuesta.json();
            alert(error.error || 'Error al buscar reservación');
            limpiarCampos();
        }
    } catch (e) {
        console.error('Error:', e);
        alert('Error de conexion');
    }
}

function limpiarCampos() {
    const campos = ['cliente', 'nombre_evento', 'descripcion', 'subtotal', 'total', 'saldo', 'reservacion_id', 'estado'];
    campos.forEach(campo => {
        const el = document.querySelector(`[data-field="${campo}"]`);
        if (el) el.value = '';
    });
}

async function registrarPago() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const reservaId = document.querySelector('[data-field="reservacion_id"]')?.value;
    const montoInput = document.querySelector('[data-field="monto"]');
    const saldoField = document.querySelector('[data-field="saldo"]');
    const nota = document.querySelector('[data-field="nota"]')?.value;
    const estado = document.querySelector('[data-field="estado"]')?.value;

    if (!reservaId) {
        alert('Primero busque una reservación válida');
        return;
    }

    // Validar que la reservación no esté en estado "Solicitada"
    if (estado && estado.toLowerCase().includes('solicitada')) {
        alert('No se puede realizar el pago porque la reservación está en estado "Solicitada". La reservación debe ser aceptada primero.');
        return;
    }

    // Convertir a números para comparación correcta
    const monto = parseFloat(montoInput?.value) || 0;
    const saldoTexto = saldoField?.value || '';
    // Extraer número del saldo (puede ser "El pago esta compleado" o un número)
    let saldo = 0;
    const match = saldoTexto.match(/([0-9]+\.?[0-9]*)/);
    if (match) {
        saldo = parseFloat(match[1]);
    }

    if (saldo === 0) {
        alert('El pago se ha completado, no hay saldo pendiente');
        return;
    }

    if (monto > saldo) {
        alert(`No puedes pagar más del saldo pendiente. Saldo actual: $${saldo.toFixed(2)}`);
        return;
    }

    if (monto <= 0) {
        alert('El monto debe ser mayor a 0');
        return;
    }

    let concepto = '';
    document.querySelectorAll('.pagos-concepto').forEach(radio => {
        if (radio.checked) concepto = radio.value;
    });

    let metodo = '';
    document.querySelectorAll('.pagos-metodo').forEach(radio => {
        if (radio.checked) metodo = radio.value;
    });

    const data = {
        reservacion: reservaId,
        monto: monto,
        nota: nota,
        concepto_pago: concepto,
        metodo_pago: metodo
    };

    abrirModalConfirmar(
        'Confirmar pago',
        `¿Confirmar el registro de un pago de $${monto.toFixed(2)}?`,
        () => ejecutarPago(data, csrfToken)
    );
}
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
async function ejecutarPago(data, csrfToken) {
    console.log('=== EJECUTANDO PAGO ===');
    console.log('Data:', data);
    console.log('CSRF Token:', getCookie('csrftoken'));
    console.log('Fetching to: /api/pago/');
    try {
        const respuesta = await fetch('/api/pago/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') || ''
            },
            body: JSON.stringify(data),
            credentials: 'same-origin'
        });

        console.log('Response status:', respuesta.status);
        console.log('Response statusText:', respuesta.statusText);
        console.log('Response ok:', respuesta.ok);
        
        if (respuesta.ok) {
            const contentType = respuesta.headers.get('content-type') || '';
            console.log('Content-Type:', contentType);
            
            const datosPago = await respuesta.json();
            console.log('Pago registrado:', datosPago);
            console.log('Servicios:', datosPago.servicios);
            console.log('Equipamentos:', datosPago.lista_equipamentos);
            console.log('Mobiliarios:', datosPago.mobiliarios);
            
            // Referencia reservación
            const now = new Date();
            const compNoEmpleado = document.getElementById('comp-no-empleado');
            const compAtendido = document.getElementById('comp-atendido');
            const compNoPago = document.getElementById('comp-no-pago');
            const compFecha = document.getElementById('comp-fecha');
            const compHora = document.getElementById('comp-hora');
            
            if (compNoEmpleado) compNoEmpleado.textContent = datosPago.no_empleado || '—';
            if (compNoPago) compNoPago.textContent = datosPago.no_pago || '1';
            if (compFecha) compFecha.textContent = now.toLocaleDateString();
            if (compHora) compHora.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            if (compAtendido) compAtendido.textContent = datosPago.atendido_por || '—';
            
            // Cliente y evento
            const compCliente = document.getElementById('comp-cliente');
            const compEvento = document.getElementById('comp-evento');
            const compFechaEvento = document.getElementById('comp-fecha-evento');
            const compHoraInicio = document.getElementById('comp-hora-inicio');
            const compHoraCierre = document.getElementById('comp-hora-cierre');
            
            const clienteInput = document.querySelector('[data-field="cliente"]')?.value;
            const clienteNombreCompleto = datosPago.cliente_nombre || clienteInput || '—';
            if (compCliente) compCliente.textContent = clienteNombreCompleto;
            if (compEvento) compEvento.textContent = document.querySelector('[data-field="nombre_evento"]')?.value || '—';
            if (compFechaEvento) compFechaEvento.textContent = datosPago.fecha_evento || '—';
            if (compHoraInicio) compHoraInicio.textContent = datosPago.hora_inicio || '—';
            if (compHoraCierre) compHoraCierre.textContent = datosPago.hora_fin || '—';
            
            // Mobiliarios
            const compMobiliarios = document.getElementById('comp-mobiliarios');
            if (compMobiliarios) {
                const mobiliarios = datosPago.mobiliarios;
                if (mobiliarios && mobiliarios.length > 0) {
                    compMobiliarios.innerHTML = mobiliarios.map(m => 
                        `<div><span class="label">${m.tipo}:</span> ${m.cantidad} pza(s)</div>`
                    ).join('');
                } else {
                    compMobiliarios.innerHTML = '<span style="color: #666;">Sin mobiliario</span>';
                }
            }
            
            // Espacio rentado
            const compSalon = document.getElementById('comp-salon');
            const compMontaje = document.getElementById('comp-montaje');
            
            if (compSalon) compSalon.textContent = datosPago.salon || '—';
            if (compMontaje) compMontaje.textContent = datosPago.montaje || '—';
            
            // Servicios y Equipamientos
            const compServicios = document.getElementById('comp-servicios');
            const compEquipamientos = document.getElementById('comp-equipamientos');
            
            if (compServicios) {
                if (datosPago.servicios && datosPago.servicios.length > 0) {
                    compServicios.innerHTML = datosPago.servicios.map(s => `<span class="item-lista">• ${s}</span>`).join('');
                } else {
                    compServicios.innerHTML = '<span style="color: #666;">Sin servicios</span>';
                }
            }
            if (compEquipamientos) {
                if (datosPago.lista_equipamentos && datosPago.lista_equipamentos.length > 0) {
                    compEquipamientos.innerHTML = datosPago.lista_equipamentos.map(e => `<span class="item-lista">• ${e}</span>`).join('');
                } else {
                    compEquipamientos.innerHTML = '<span style="color: #666;">Sin equipamentos</span>';
                }
            }
            
            // Datos financieros
            const compMonto = document.getElementById('comp-monto');
            const compSubtotal = document.getElementById('comp-subtotal');
            const compIva = document.getElementById('comp-iva');
            const compTotal = document.getElementById('comp-total');
            const compSaldo = document.getElementById('comp-saldo');
            
            if (compMonto) compMonto.textContent = '$' + data.monto;
            if (compSubtotal) compSubtotal.textContent = '$' + (datosPago.subtotal || '0.00');
            if (compIva) compIva.textContent = '$' + (datosPago.iva || '0.00');
            if (compTotal) compTotal.textContent = '$' + (datosPago.total || '0.00');
            if (compSaldo) compSaldo.textContent = '$' + (parseFloat(datosPago.saldo || 0)).toFixed(2);
            
            // Mostrar modal de comprobante
            const modalComprobante = document.getElementById('modal-comprobante');
            if (modalComprobante) {
                modalComprobante.showModal();
            } else {
                alert('Pago registrado exitosamente');
            }
            
            // Cerrar modal de pagos
            const modal = document.getElementById('modalPagos');
            if (modal) modal.close();
        } else {
            console.log('Response no OK, status:', respuesta.status);
            // Leer respuesta solo una vez
            const contentType = respuesta.headers.get('content-type') || '';
            if (contentType.includes('application/json')) {
                const error = await respuesta.json();
                console.log('Error response:', error);
                alert(error.error || error.mensaje || Object.values(error).join(', ') || 'Error al registrar pago');
            } else {
                const text = await respuesta.text();
                console.log('Error HTML:', text.substring(0, 500));
                alert('Error del servidor (500). Revisa la consola del servidor.');
            }
        }
    } catch (e) {
        console.error('Catch error:', e);
        alert('Error de conexión: ' + e.message);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const btnBuscar = document.getElementById('btn-buscar-reservacion');
    if (btnBuscar) {
        btnBuscar.addEventListener('click', buscarReservacion);
    }
    
    const btnConfirmar = document.getElementById('btn-confirmar-pago');
    if (btnConfirmar) {
        btnConfirmar.addEventListener('click', registrarPago);
    }
    
    const btnCancelar = document.getElementById('btn-cancelar-pago');
    if (btnCancelar) {
        btnCancelar.addEventListener('click', () => {
            const modal = document.getElementById('modalPagos');
            if (modal) modal.close();
        });
    }
});

function generarPDF() {
    const container = document.querySelector('#comprobante-content');
    if (!container) {
        alert('Error: No se encontró el contenido del comprobante');
        return;
    }
    
    const fecha = new Date().toISOString().slice(0, 10);
    const opt = {
        margin: [0, 0, 0, 0],
        filename: `comprobante_pago_${fecha}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { 
            scale: 2, 
            y: 0, 
            scrollY: 0,
            useCORS: true,
            backgroundColor: '#ffffff'
        },
        jsPDF: { unit: 'mm', format: 'a5', orientation: 'portrait' }
    };
    
    html2pdf().set(opt).from(container).save();
}
