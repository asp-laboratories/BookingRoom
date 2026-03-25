function getPagosContainer() {
    return document.getElementById('modalPagos') || document.querySelector('.pagos-container');
}

function queryField(selector) {
    const container = getPagosContainer();
    return container ? container.querySelector(`[data-field="${selector}"]`) : null;
}

async function buscarReservacion() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const numero = queryField('reservacion')?.value;
    
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
            const setVal = (field, val) => {
                const el = queryField(field);
                if (el) el.value = val || '';
            };
            setVal('cliente', datos.cliente);
            setVal('nombre_evento', datos.nombre_evento);
            setVal('descripcion', datos.descripcion);
            setVal('subtotal', datos.subtotal);
            setVal('total', datos.total);
            setVal('saldo', datos.saldo_restante);
            setVal('reservacion_id', datos.id);
            setVal('estado', datos.estado);
        } else {
            const error = await respuesta.json();
            alert(error.error || 'Error al buscar reservación');
            limpiarCampos();
        }
    } catch {
        alert('Error de conexion');
    }
}

function limpiarCampos() {
    const campos = ['cliente', 'nombre_evento', 'descripcion', 'subtotal', 'total', 'saldo', 'reservacion_id', 'estado'];
    campos.forEach(campo => {
        const el = queryField(campo);
        if (el) el.value = '';
    });
}

async function registrarPago() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    const reservaId = queryField('reservacion_id')?.value;
    const monto = queryField('monto')?.value;
    const nota = queryField('nota')?.value;

    if (!reservaId) {
        alert('Primero busque una reservación válida');
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
