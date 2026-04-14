// JavaScript específico para la página de reservación de cliente
// Autocompletar datos del cliente si ya existen en la base de datos

document.addEventListener('DOMContentLoaded', function() {
    // Iniciar carga de datos
    cargarDatosCliente();
    
    // Botón registrar cliente
    const btnRegistrarCliente = document.getElementById('btn-registrar-cliente');
    if (btnRegistrarCliente) {
        btnRegistrarCliente.addEventListener('click', async function() {
            await guardarDatosCliente();
        });
    }
    
    // Radio buttons tipo de cliente
    document.querySelectorAll('input[name="tipo-cliente"]').forEach(radio => {
        radio.addEventListener('change', function() {
            actualizarLabelsCliente(this.value);
        });
    });
    
    // Auto-trim en campos de texto al perder foco
    document.querySelectorAll('.cliente-input').forEach(input => {
        input.addEventListener('blur', function() {
            this.value = this.value.trim();
        });
    });
});

/**
 * Cargar datos del cliente desde la API al cargar la página
 */
async function cargarDatosCliente() {
    const email = window.CLIENTE_EMAIL;
    if (!email) {
        console.log('No hay email del cliente');
        return;
    }
    
    try {
        const response = await fetch(`/api/perfil/?email=${encodeURIComponent(email)}`);
        
        if (!response.ok) {
            console.log('No se pudieron cargar los datos del cliente, status:', response.status);
            return;
        }
        
        const data = await response.json();
        console.log('Datos del cliente desde API:', data);
        console.log('tipo_usuario:', data.tipo_usuario);
        console.log('rfc:', data.rfc);
        
        // Si el cliente ya tiene datos (tipo_usuario === 'cliente' y tiene rfc o id), autocompletar
        if (data.tipo_usuario === 'cliente' && (data.rfc || data.id)) {
            console.log('Cliente con datos existentes, autocompletando...');
            
            document.getElementById('cliente-rfc').value = data.rfc || '';
            document.getElementById('cliente-nombre').value = data.nombre || '';
            document.getElementById('cliente-apellido-paterno').value = data.apellidoPaterno || '';
            document.getElementById('cliente-apellido-materno').value = data.apelidoMaterno || '';
            document.getElementById('cliente-nombre-fiscal').value = data.nombre_fiscal || '';
            document.getElementById('cliente-colonia').value = data.dir_colonia || '';
            document.getElementById('cliente-calle').value = data.dir_calle || '';
            document.getElementById('cliente-numero').value = data.dir_numero || '';
            document.getElementById('cliente-telefono').value = data.telefono || '';
            document.getElementById('cliente-correo').value = data.correo_electronico || '';
            
            // Habilitar y marcar como autollenado
            document.querySelectorAll('.cliente-input').forEach(input => {
                input.disabled = false;
                input.classList.add('autollenado');
            });
            
            // Determinar tipo de cliente
            const tipoClienteId = data.tipo_cliente_id;
            if (tipoClienteId) {
                const id = parseInt(tipoClienteId);
                const tipoRadio = id > 1 ? 'tipo-moral' : 'tipo-fisica';
                const radio = document.getElementById(tipoRadio);
                if (radio) {
                    radio.checked = true;
                    radio.disabled = false;
                    actualizarLabelsCliente(id > 1 ? 'moral' : 'fisica');
                }
            }
            
            // Deshabilitar botón de registrar ya que ya tiene datos
            const btnRegistrar = document.getElementById('btn-registrar-cliente');
            if (btnRegistrar) {
                btnRegistrar.disabled = true;
            }
            
            console.log('Datos del cliente cargados exitosamente');
        } else {
            console.log('Cliente sin datos registrados, habilitando campos...');
            // Si no tiene datos, habilitar campos para que los llene
            habilitarCamposCliente();
        }
        
    } catch (error) {
        console.error('Error al cargar datos del cliente:', error);
    }
}

/**
 * Guardar datos del cliente en la API
 */
async function guardarDatosCliente() {
    const email = window.CLIENTE_EMAIL;
    if (!email) {
        mostrarToastExito('No hay sesión activa', 'error');
        return;
    }
    
    const rfc = document.getElementById('cliente-rfc').value.trim();
    const nombre = document.getElementById('cliente-nombre').value.trim();
    const apellidoPaterno = document.getElementById('cliente-apellido-paterno').value.trim();
    const apellidoMaterno = document.getElementById('cliente-apellido-materno').value.trim();
    const nombreFiscal = document.getElementById('cliente-nombre-fiscal').value.trim();
    const colonia = document.getElementById('cliente-colonia').value.trim();
    const calle = document.getElementById('cliente-calle').value.trim();
    const numero = document.getElementById('cliente-numero').value.trim();
    const telefono = document.getElementById('cliente-telefono').value.trim();
    
    // Validaciones básicas
    if (!rfc) {
        mostrarToastExito('El RFC es obligatorio', 'warning');
        return;
    }
    if (!nombre) {
        mostrarToastExito('El nombre es obligatorio', 'warning');
        return;
    }
    if (!apellidoPaterno) {
        mostrarToastExito('El apellido paterno es obligatorio', 'warning');
        return;
    }
    if (!telefono) {
        mostrarToastExito('El teléfono es obligatorio', 'warning');
        return;
    }
    
    const datos = {
        rfc: rfc,
        nombre: nombre,
        apellidoPaterno: apellidoPaterno,
        apelidoMaterno: apellidoMaterno,
        nombre_fiscal: nombreFiscal,
        dir_colonia: colonia,
        dir_calle: calle,
        dir_numero: numero,
        telefono: telefono,
        correo_electronico: email
    };
    
    console.log('Guardando datos del cliente:', datos);
    
    try {
        const response = await fetch(`/api/perfil/?email=${encodeURIComponent(email)}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error del API:', errorData);
            mostrarToastExito(errorData.error || 'Error al guardar datos', 'error');
            return;
        }
        
        const data = await response.json();
        console.log('Datos guardados exitosamente:', data);
        
        mostrarToastExito('Datos del cliente guardados exitosamente', 'success');
        
        // Deshabilitar campos y botón después de guardar
        document.querySelectorAll('.cliente-input').forEach(input => {
            input.disabled = true;
            input.classList.add('autollenado');
        });
        
        const btnRegistrar = document.getElementById('btn-registrar-cliente');
        if (btnRegistrar) {
            btnRegistrar.disabled = true;
        }
        
    } catch (error) {
        console.error('Error al guardar datos:', error);
        mostrarToastExito('Error de conexión al guardar datos', 'error');
    }
}

/**
 * Habilitar campos para edición
 */
function habilitarCamposCliente() {
    document.querySelectorAll('.cliente-input').forEach(input => {
        input.disabled = false;
    });
    
    document.querySelectorAll('input[name="tipo-cliente"]').forEach(radio => {
        radio.disabled = false;
    });
    
    const btnRegistrar = document.getElementById('btn-registrar-cliente');
    if (btnRegistrar) {
        btnRegistrar.disabled = false;
    }
}

/**
 * Actualizar labels según tipo de cliente
 */
function actualizarLabelsCliente(tipo) {
    const labelNombre = document.getElementById('label-nombre-contacto');
    const labelNombreFiscal = document.getElementById('label-nombre-fiscal');
    const nombreInput = document.getElementById('cliente-nombre');
    
    if (tipo === 'moral') {
        labelNombre.textContent = 'Nombre del contacto';
        labelNombreFiscal.textContent = 'Nombre de la empresa';
        if (nombreInput) {
            nombreInput.placeholder = 'Ej: María López';
        }
    } else {
        labelNombre.textContent = 'Nombre completo';
        labelNombreFiscal.textContent = 'Nombre Fiscal';
        if (nombreInput) {
            nombreInput.placeholder = 'Ej: Juan Pérez García';
        }
    }
}
