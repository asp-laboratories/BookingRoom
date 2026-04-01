
let inlineEditConfig = null;
let datosOriginales = {};
let editando = false;

function configurarInlineEdit(config) {
    inlineEditConfig = config;
}

function editarRegistro(id) {
    if (!inlineEditConfig) return;
    if (editando) return;
    
    editando = true;
    deshabilitarBotonesEditar();
    
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) {
        editando = false;
        habilitarBotonesEditar();
        return;
    }
    
    datosOriginales[id] = {};
    inlineEditConfig.campos.forEach(campo => {
        const dataAttr = campo.dataAttr || campo.nombre;
        datosOriginales[id][campo.nombre] = row.dataset[dataAttr] || row.querySelector(`.${campo.clase}`)?.textContent?.trim() || '';
    });
    
    row.classList.add('inline-edicion');
    
    inlineEditConfig.campos.forEach(campo => {
        const celda = row.querySelector(`.${campo.clase}`);
        if (!celda) return;
        
        const dataAttr = campo.dataAttr || campo.nombre;
        const valor = row.dataset[dataAttr] || celda.textContent.trim();
        
        if (campo.tipo === 'texto') {
            celda.innerHTML = `<input type="text" class="inline-input" data-campo="${campo.nombre}" value="${valor}">`;
        } else if (campo.tipo === 'numero') {
            celda.innerHTML = `<input type="number" step="0.01" class="inline-input" data-campo="${campo.nombre}" value="${valor}">`;
        } else if (campo.tipo === 'entero') {
            celda.innerHTML = `<input type="number" step="1" class="inline-input" data-campo="${campo.nombre}" value="${valor}">`;
        } else if (campo.tipo === 'select') {
            celda.innerHTML = `
                <select class="inline-input" data-campo="${campo.nombre}">
                    ${campo.opciones.map(op => 
                        `<option value="${op.valor}" ${valor === op.valor ? 'selected' : ''}>${op.texto}</option>`
                    ).join('')}
                </select>
            `;
        } else if (campo.tipo === 'booleano') {
            celda.innerHTML = `
                <select class="inline-input" data-campo="${campo.nombre}">
                    <option value="true" ${valor === 'true' || valor === '1' ? 'selected' : ''}>Activo</option>
                    <option value="false" ${valor === 'false' || valor === '0' ? 'selected' : ''}>Inactivo</option>
                </select>
            `;
        } else if (campo.tipo === 'select-db') {
            // Para selects que cargan opciones desde Django
            celda.innerHTML = `
                <select class="inline-input" data-campo="${campo.nombre}">
                    ${window[`${campo.opcionesVar}`]?.map(op => 
                        `<option value="${op.id || op.codigo}" ${valor == (op.id || op.codigo) ? 'selected' : ''}>${op.nombre}</option>`
                    ).join('') || ''}
                </select>
            `;
        }
    });
    
    const btnEditar = row.querySelector('.btn-editar');
    const btnGuardar = row.querySelector('.btn-guardar');
    const btnCancelar = row.querySelector('.btn-cancelar');
    
    if (btnEditar) btnEditar.style.display = 'none';
    if (btnGuardar) btnGuardar.style.display = 'inline-block';
    if (btnCancelar) btnCancelar.style.display = 'inline-block';
    
    row.querySelectorAll('.inline-input').forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                guardarRegistro(id);
            }
        });
    });
}

function guardarRegistro(id) {
    if (!inlineEditConfig) return;
    
    const row = document.querySelector(`tr[data-id="${id}"]`);
    if (!row) return;
    
    const datos = {};
    let valido = true;
    
    row.querySelectorAll('.inline-input').forEach(input => {
        const campo = input.dataset.campo;
        let valor = input.value;
        
        if (input.type === 'number') {
            valor = valor || '0';
        }
        
        if (campo === inlineEditConfig.campoObligatorio && !valor) {
            valido = false;
        }
        
        datos[campo] = valor;
    });
    
    if (!valido) {
        mostrarToastExito('Complete todos los campos requeridos', 'error');
        return;
    }
    
    const nombre = datos[inlineEditConfig.campoNombre] || `registro ${id}`;
    abrirModalConfirmar(
        'Confirmar cambios',
        `¿Deseas actualizar ${inlineEditConfig.nombreSingular} "${nombre}"?`,
        function() {
            enviarActualizacion(id, datos);
        }
    );
}

function enviarActualizacion(id, datos) {
    if (!inlineEditConfig) return;
    
    const formData = new FormData();
    Object.keys(datos).forEach(key => {
        formData.append(key, datos[key]);
    });
    
    const url = inlineEditConfig.urlActualizar.replace('0', id);
    
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
        }
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            window.location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        mostrarToastExito('Error al guardar los cambios', 'error');
    });
}

function cancelarEdicionInline(id) {
    if (!inlineEditConfig) {
        window.location.reload();
        return;
    }
    
    abrirModalCancelar(
        'Cancelar edición',
        '¿Estás seguro de que quieres cancelar los cambios?',
        function() {
            editando = false;
            habilitarBotonesEditar();
            window.location.reload();
        }
    );
}

function deshabilitarBotonesEditar() {
    document.querySelectorAll('.btn-editar').forEach(btn => {
        btn.disabled = true;
        btn.style.opacity = '0.5';
        btn.style.cursor = 'not-allowed';
    });
}

function habilitarBotonesEditar() {
    document.querySelectorAll('.btn-editar').forEach(btn => {
        btn.disabled = false;
        btn.style.opacity = '1';
        btn.style.cursor = 'pointer';
    });
}

const inlineEditStyles = document.createElement('style');
inlineEditStyles.textContent = `
    .inline-edicion td {
        background-color: #f8f9fa;
    }
    
    .inline-input {
        width: 100%;
        padding: 5px;
        border: 1px solid #ced4da;
        border-radius: 4px;
        font-size: 14px;
        box-sizing: border-box;
    }
    
    .inline-input:focus {
        outline: none;
        border-color: #86b7fe;
        box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25);
    }
`;
document.head.appendChild(inlineEditStyles);