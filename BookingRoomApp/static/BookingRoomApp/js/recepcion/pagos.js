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
    const monto = document.querySelector('[data-field="monto"]')?.value;
    const saldo = document.querySelector('[data-field="saldo"]')?.value;
    const nota = document.querySelector('[data-field="nota"]')?.value;

    if (!reservaId) {
        alert('Primero busque una reservación válida');
        return;
    }

    if(monto > saldo){
        alert('No puedes pagar mas');
        return
    }

    if(saldo == 0){
        alert('El pago se ha compleado, no hay saldo');
        return
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

    console.log(reservaId);
    console.log(monto);
    console.log(nota);
    console.log(concepto);
    console.log(metodo);
    

    try {
        const respuesta = await fetch('/api/pago/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken || ''
            },
            body: JSON.stringify(data),
            credentials: 'same-origin'
        });

        if (respuesta.ok) {
            alert('Pago registrado exitosamente');
            const modal = document.getElementById('modalPagos');
            if (modal) modal.close();
            location.reload();
        } else {
            const error = await respuesta.json();
            alert(error.error || error.mensaje || 'Error al registrar pago');
            console.log(error.error);
            
        }
    } catch {
        alert('Error de conexion');
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
