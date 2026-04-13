// Validaciones para el formulario de registro de cliente

document.addEventListener("DOMContentLoaded", function() {
    const clienteInputs = document.querySelectorAll('.cliente-input');
    const rfcInput = document.getElementById('cliente-rfc');
    const nombreInput = document.getElementById('cliente-nombre');
    const apellidoPaternoInput = document.getElementById('cliente-apellido-paterno');
    const apellidoMaternoInput = document.getElementById('cliente-apellido-materno');
    const nombreFiscalInput = document.getElementById('cliente-nombre-fiscal');
    const coloniaInput = document.getElementById('cliente-colonia');
    const calleInput = document.getElementById('cliente-calle');
    const numeroInput = document.getElementById('cliente-numero');
    const telefonoInput = document.getElementById('cliente-telefono');
    const correoInput = document.getElementById('cliente-correo');
    const tipoMoral = document.getElementById('tipo-moral');
    const tipoFisica = document.getElementById('tipo-fisica');

    // ==========================================
    // RFC VALIDATION
    // ==========================================
    
    // Validación simplificada para pruebas: mínimo 10, máximo 13 caracteres
    // La validación completa está comentada para uso futuro
    function validarRFC(rfc) {
        if (!rfc || rfc.trim() === '') {
            return { valido: false, mensaje: 'El RFC es obligatorio' };
        }
        
        // Convertir a mayúsculas
        rfc = rfc.toUpperCase();
        
        // Validación simplificada para pruebas
        if (rfc.length < 10 || rfc.length > 13) {
            return { valido: false, mensaje: 'El RFC debe tener entre 10 y 13 caracteres' };
        }
        
        // Validación completa comentada (formato mexicano real):
        // if (!/^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$/.test(rfc)) {
        //     return { valido: false, mensaje: 'El RFC no tiene un formato válido (ejemplo: ABCD123456XYZ)' };
        // }
        
        return { valido: true, mensaje: 'RFC válido' };
    }

    // Auto-formatear RFC mientras se escribe
    if (rfcInput) {
        rfcInput.addEventListener('input', function() {
            // Convertir a mayúsculas automáticamente
            this.value = this.value.toUpperCase();
            
            // Limitar a 13 caracteres
            if (this.value.length > 13) {
                this.value = this.value.slice(0, 13);
            }
            
            // Solo permitir caracteres alfanuméricos
            this.value = this.value.replace(/[^A-Z0-9Ñ&]/g, '');
        });

        // Validar al perder el foco
        rfcInput.addEventListener('blur', function() {
            if (this.value && this.value.trim() !== '') {
                const validacion = validarRFC(this.value);
                if (!validacion.valido) {
                    mostrarToastExito(validacion.mensaje, 'warning');
                }
            }
        });
    }

    // ==========================================
    // NOMBRE FISCAL AUTO-ACTUALIZACIÓN
    // ==========================================
    
    // Para persona física: Nombre Fiscal = Nombre + Apellido Paterno + Apellido Materno
    // No se puede editar manualmente
    function actualizarNombreFiscal() {
        const tipoSeleccionado = tipoMoral?.checked ? 'moral' : tipoFisica?.checked ? 'fisica' : null;
        
        if (!nombreFiscalInput) return;
        
        if (tipoSeleccionado === 'fisica') {
            // Persona física: nombre fiscal = nombre completo
            const nombre = nombreInput?.value || '';
            const apellidoPaterno = apellidoPaternoInput?.value || '';
            const apellidoMaterno = apellidoMaternoInput?.value || '';
            
            const nombreCompleto = [nombre, apellidoPaterno, apellidoMaterno]
                .filter(part => part.trim() !== '')
                .join(' ');
            
            nombreFiscalInput.value = nombreCompleto;
            nombreFiscalInput.readOnly = true; // No editable
            nombreFiscalInput.style.backgroundColor = '#f5f5f5';
            nombreFiscalInput.style.cursor = 'not-allowed';
            nombreFiscalInput.placeholder = 'Se genera automáticamente';
            
        } else if (tipoSeleccionado === 'moral') {
            // Persona moral: nombre fiscal es el nombre de la empresa (editable)
            nombreFiscalInput.readOnly = false;
            nombreFiscalInput.style.backgroundColor = '';
            nombreFiscalInput.style.cursor = '';
            nombreFiscalInput.placeholder = 'Ej: Empresa ABC S.A. de C.V.';
        }
    }

    // Event listeners para actualizar nombre fiscal en tiempo real
    if (nombreInput) {
        nombreInput.addEventListener('input', actualizarNombreFiscal);
    }
    if (apellidoPaternoInput) {
        apellidoPaternoInput.addEventListener('input', actualizarNombreFiscal);
    }
    if (apellidoMaternoInput) {
        apellidoMaternoInput.addEventListener('input', actualizarNombreFiscal);
    }

    // ==========================================
    // TELÉFONO VALIDATION
    // ==========================================
    
    if (telefonoInput) {
        telefonoInput.addEventListener('input', function() {
            // Solo permitir números
            this.value = this.value.replace(/[^0-9]/g, '');
            
            // Limitar a 10 dígitos
            if (this.value.length > 10) {
                this.value = this.value.slice(0, 10);
            }
        });

        telefonoInput.addEventListener('blur', function() {
            if (this.value && this.value.trim() !== '') {
                if (!/^\d{10}$/.test(this.value)) {
                    mostrarToastExito('El teléfono debe tener exactamente 10 dígitos', 'warning');
                }
            }
        });
    }

    // ==========================================
    // CORREO VALIDATION
    // ==========================================
    
    function validarCorreo(correo) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(correo);
    }

    if (correoInput) {
        // Auto-trim al perder foco
        correoInput.addEventListener('blur', function() {
            this.value = this.value.trim();
            
            if (this.value && this.value.trim() !== '') {
                if (!validarCorreo(this.value)) {
                    mostrarToastExito('El correo electrónico no tiene un formato válido', 'warning');
                }
            }
        });
    }

    // ==========================================
    // NÚMERO DE DIRECCIÓN VALIDATION
    // ==========================================
    
    if (numeroInput) {
        numeroInput.addEventListener('input', function() {
            // Solo permitir números
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }

    // ==========================================
    // CAMPOS DE TEXTO VALIDATION
    // ==========================================
    
    // Auto-trim en todos los campos de texto al perder foco
    [nombreInput, apellidoPaternoInput, apellidoMaternoInput, coloniaInput, calleInput].forEach(input => {
        if (input) {
            input.addEventListener('blur', function() {
                this.value = this.value.trim();
            });
        }
    });

    // ==========================================
    // TIPO DE CLIENTE CHANGE HANDLER
    // ==========================================
    
    function onTipoClienteChange() {
        actualizarNombreFiscal();
        
        const tipoSeleccionado = tipoMoral?.checked ? 'moral' : tipoFisica?.checked ? 'fisica' : null;
        
        if (tipoSeleccionado === 'moral') {
            // Cambiar labels para empresa
            document.getElementById('label-nombre-contacto').textContent = 'Nombre del contacto';
            document.getElementById('label-nombre-fiscal').textContent = 'Nombre de la empresa';
            
            // Auto-llenar nombre fiscal con el nombre del contacto
            if (nombreInput && nombreFiscalInput && !nombreFiscalInput.value) {
                nombreFiscalInput.value = nombreInput.value;
            }
            
        } else if (tipoSeleccionado === 'fisica') {
            // Cambiar labels para persona física
            document.getElementById('label-nombre-contacto').textContent = 'Nombre completo';
            document.getElementById('label-nombre-fiscal').textContent = 'Nombre Fiscal';
            
            // Actualizar nombre fiscal automáticamente
            actualizarNombreFiscal();
        }
    }

    if (tipoMoral) {
        tipoMoral.addEventListener('change', onTipoClienteChange);
    }
    if (tipoFisica) {
        tipoFisica.addEventListener('change', onTipoClienteChange);
    }

    // ==========================================
    // VALIDACIÓN AL REGISTRAR CLIENTE
    // ==========================================
    
    const btnRegistrarCliente = document.getElementById('btn-registrar-cliente');
    
    if (btnRegistrarCliente) {
        const clickHandlerOriginal = btnRegistrarCliente.onclick;
        
        btnRegistrarCliente.addEventListener('click', function(e) {
            let errores = [];
            
            // Validar RFC
            if (rfcInput && rfcInput.value) {
                const rfcValidacion = validarRFC(rfcInput.value);
                if (!rfcValidacion.valido) {
                    errores.push(rfcValidacion.mensaje);
                }
            }
            
            // Validar teléfono
            if (telefonoInput && telefonoInput.value) {
                if (!/^\d{10}$/.test(telefonoInput.value)) {
                    errores.push('El teléfono debe tener exactamente 10 dígitos');
                }
            }
            
            // Validar correo
            if (correoInput && correoInput.value) {
                if (!validarCorreo(correoInput.value)) {
                    errores.push('El correo electrónico no tiene un formato válido');
                }
            }
            
            // Validar campos obligatorios
            const camposObligatorios = [
                { input: rfcInput, nombre: 'RFC' },
                { input: nombreInput, nombre: 'Nombre' },
                { input: apellidoPaternoInput, nombre: 'Apellido paterno' },
                { input: nombreFiscalInput, nombre: 'Nombre fiscal' },
                { input: coloniaInput, nombre: 'Colonia' },
                { input: calleInput, nombre: 'Calle' },
                { input: numeroInput, nombre: 'Número' },
                { input: telefonoInput, nombre: 'Teléfono' },
                { input: correoInput, nombre: 'Correo' }
            ];
            
            camposObligatorios.forEach(campo => {
                if (campo.input && (!campo.input.value || campo.input.value.trim() === '')) {
                    errores.push(`El campo "${campo.nombre}" es obligatorio`);
                }
            });
            
            // Mostrar errores si los hay
            if (errores.length > 0) {
                e.preventDefault();
                e.stopImmediatePropagation();
                mostrarToastExito('Errores en el formulario:\n\n• ' + errores.join('\n• '), 'error');
                return false;
            }
            
            // Si todo está válido, continuar con el registro
            return true;
        }, true); // Capturing phase para interceptar antes
    }
});
