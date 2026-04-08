document.addEventListener("DOMContentLoaded", () => {
  // Overlay de notificaciones
  const overlay = document.getElementById("reservacion-overlay");
  const abrir = document.querySelector(".expandir-solicitud");
  const cerrar = document.getElementById("reservacion-cerrar");

  if (abrir) {
    abrir.addEventListener("click", (e) => {
      e.preventDefault();
      overlay.classList.add("mostrar");
    });
  }

  if (cerrar) {
    cerrar.addEventListener("click", () => {
      overlay.classList.remove("mostrar");
    });
  }

  if (overlay) {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("mostrar");
      }
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && overlay && overlay.classList.contains("mostrar")) {
      overlay.classList.remove("mostrar");
    }
  });

  // Navegación con scroll suave
  document.querySelectorAll('.reservacion-navegacion a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      const targetElement = document.querySelector(targetId);
      
      if (targetElement) {
        const headerHeight = document.querySelector('.reservacion-contenedor-navegacion')?.offsetHeight || 0;
        const windowHeight = window.innerHeight;
        const elementHeight = targetElement.offsetHeight;
        
        const targetPosition = targetElement.offsetTop - (windowHeight / 2) + (elementHeight / 2);
        
        window.scrollTo({
          top: Math.max(0, targetPosition - headerHeight - 20),
          behavior: 'smooth'
        });
      }
    });
  });

  // Elementos del formulario cliente
  const btnBuscarCliente = document.getElementById('btn-buscar-cliente');
  const buscarInput = document.getElementById('buscar-cliente-input');
  const clienteInputs = document.querySelectorAll('.cliente-input');
  const tipoMoral = document.getElementById('tipo-moral');
  const tipoFisica = document.getElementById('tipo-fisica');
  const radioButtons = document.querySelectorAll('input[name="tipo-cliente"]');
  const btnRegistrarCliente = document.getElementById('btn-registrar-cliente');

  // Labels para cambiar según tipo de cliente
  const labelNombreContacto = document.getElementById('label-nombre-contacto');
  const labelApellidoPaterno = document.getElementById('label-apellido-paterno');
  const labelApellidoMaterno = document.getElementById('label-apellido-materno');
  const labelNombreFiscal = document.getElementById('label-nombre-fiscal');
  const campoApellidoPaterno = document.getElementById('campo-apellido-paterno');
  const campoApellidoMaterno = document.getElementById('campo-apellido-materno');

  function cambiarLabelsCliente(tipo) {
    const nombreInput = document.getElementById('cliente-nombre');
    
    if (tipo === 'moral') {
      labelNombreContacto.textContent = 'Nombre del contacto';
      labelApellidoPaterno.textContent = 'Primer apellido del contacto';
      labelApellidoMaterno.textContent = 'Segundo apellido del contacto';
      labelNombreFiscal.textContent = 'Nombre de la empresa';
      campoApellidoPaterno.style.display = '';
      campoApellidoMaterno.style.display = '';
      
      if (nombreInput) {
        nombreInput.placeholder = 'Ej: María López';
      }
    } else {
      labelNombreContacto.textContent = 'Nombre completo';
      labelApellidoPaterno.textContent = 'Primer apellido';
      labelApellidoMaterno.textContent = 'Segundo apellido';
      labelNombreFiscal.textContent = 'Nombre Fiscal';
      campoApellidoPaterno.style.display = '';
      campoApellidoMaterno.style.display = '';
      
      if (nombreInput) {
        nombreInput.placeholder = 'Ej: Juan Pérez García';
      }
    }
  }

  function habilitarInputsCliente() {
    clienteInputs.forEach(input => {
      input.disabled = false;
    });
    radioButtons.forEach(radio => {
      radio.disabled = false;
    });
    if (btnRegistrarCliente) {
      btnRegistrarCliente.disabled = false;
    }
  }

  function deshabilitarInputsCliente() {
    clienteInputs.forEach(input => {
      input.disabled = true;
    });
    radioButtons.forEach(radio => {
      radio.disabled = true;
    });
    if (btnRegistrarCliente) {
      btnRegistrarCliente.disabled = true;
    }
  }

  function limpiarInputsCliente() {
    const nombreInput = document.getElementById('cliente-nombre');
    
    clienteInputs.forEach(input => {
      input.value = '';
    });
    radioButtons.forEach(radio => {
      radio.checked = false;
    });
    document.querySelectorAll('.cliente-input').forEach(input => {
      input.classList.remove('autollenado');
    });
    cambiarLabelsCliente('fisica');
    
    // Restaurar placeholder del nombre
    if (nombreInput) {
      nombreInput.placeholder = 'Ej: Juan Pérez García';
    }
  }

  // Event listeners para los radio buttons
  radioButtons.forEach(radio => {
    radio.addEventListener('change', function() {
      if (this.checked) {
        const tipo = this.value;
        const nombreInput = document.getElementById('cliente-nombre');
        const nombreFiscalInput = document.getElementById('cliente-nombre-fiscal');
        
        cambiarLabelsCliente(tipo);
        
        if (tipo === 'moral') {
          if (nombreInput) {
            nombreInput.placeholder = 'Ej: María López';
            nombreFiscalInput.value = nombreInput.value;
          }
        } else {
          if (nombreInput) {
            nombreInput.placeholder = 'Ej: Juan Pérez García';
          }
        }
      }
    });
  });

  // Auto-llenar nombre fiscal cuando se escribe en nombre (solo si es empresa)
  const nombreInputEl = document.getElementById('cliente-nombre');
  if (nombreInputEl) {
    nombreInputEl.addEventListener('input', function() {
      if (tipoMoral && tipoMoral.checked) {
        const nombreFiscalInput = document.getElementById('cliente-nombre-fiscal');
        if (nombreFiscalInput) {
          nombreFiscalInput.value = this.value;
        }
      }
    });
  }

  // Botón buscar cliente
  if (btnBuscarCliente) {
    btnBuscarCliente.addEventListener('click', async function() {
      const query = buscarInput.value.trim();
      
      if (!query) {
        mostrarToastExito('Ingrese un RFC o nombre para buscar', 'warning');
        return;
      }

      try {
        const response = await fetch(`/reservacion/buscar-cliente/?q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data.encontrado) {
          document.getElementById('cliente-rfc').value = data.cliente.rfc || '';
          document.getElementById('cliente-nombre').value = data.cliente.nombre || '';
          document.getElementById('cliente-apellido-paterno').value = data.cliente.apellido_paterno || '';
          document.getElementById('cliente-apellido-materno').value = data.cliente.apellido_materno || '';
          document.getElementById('cliente-nombre-fiscal').value = data.cliente.nombre_fiscal || '';
          document.getElementById('cliente-colonia').value = data.cliente.colonia || '';
          document.getElementById('cliente-calle').value = data.cliente.calle || '';
          document.getElementById('cliente-numero').value = data.cliente.numero || '';
          document.getElementById('cliente-telefono').value = data.cliente.telefono || '';
          document.getElementById('cliente-correo').value = data.cliente.correo || '';
          
          document.querySelectorAll('.cliente-input').forEach(input => {
            input.classList.add('autollenado');
          });
          
          radioButtons.forEach(radio => radio.checked = false);
          if (data.cliente.tipo_cliente) {
            if (data.cliente.tipo_cliente.toLowerCase().includes('moral') || data.cliente.tipo_cliente.toLowerCase().includes('empresa')) {
              tipoMoral.checked = true;
              cambiarLabelsCliente('moral');
            } else {
              tipoFisica.checked = true;
              cambiarLabelsCliente('fisica');
            }
          }
          
          deshabilitarInputsCliente();
          if (btnRegistrarCliente) btnRegistrarCliente.disabled = true;
          mostrarToastExito('Cliente encontrado', 'success');
        } else {
          habilitarInputsCliente();
          limpiarInputsCliente();
          
          document.getElementById('cliente-rfc').value = query;
          document.getElementById('cliente-rfc').disabled = false;

          mostrarToastExito(data.mensaje + '. Complete los datos del cliente', 'warning');
        }
      } catch (error) {
        console.error('Error:', error);
        mostrarToastExito('Error al buscar cliente', 'error');
      }
    });
  }

  if (buscarInput) {
    buscarInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (btnBuscarCliente) btnBuscarCliente.click();
      }
    });
  }

  // Botón registrar cliente
  if (btnRegistrarCliente) {
    btnRegistrarCliente.addEventListener('click', async function() {
      const rfcInput = document.getElementById('cliente-rfc');
      const rfcValue = rfcInput.value.trim();
      
      if (!rfcValue) {
        mostrarToastExito('Ingrese el RFC del cliente', 'warning');
        return;
      }

      let tipoSeleccionado = null;
      radioButtons.forEach(radio => {
        if (radio.checked) tipoSeleccionado = radio.value;
      });

      if (!tipoSeleccionado) {
        mostrarToastExito('Seleccione el tipo de cliente (Empresa o Persona física)', 'warning');
        return;
      }

      try {
        const response = await fetch(`/reservacion/buscar-cliente/?q=${encodeURIComponent(rfcValue)}`);
        const data = await response.json();

        if (data.encontrado) {
          document.getElementById('cliente-nombre').value = data.cliente.nombre || '';
          document.getElementById('cliente-apellido-paterno').value = data.cliente.apellido_paterno || '';
          document.getElementById('cliente-apellido-materno').value = data.cliente.apellido_materno || '';
          document.getElementById('cliente-nombre-fiscal').value = data.cliente.nombre_fiscal || '';
          document.getElementById('cliente-colonia').value = data.cliente.colonia || '';
          document.getElementById('cliente-calle').value = data.cliente.calle || '';
          document.getElementById('cliente-numero').value = data.cliente.numero || '';
          document.getElementById('cliente-telefono').value = data.cliente.telefono || '';
          document.getElementById('cliente-correo').value = data.cliente.correo || '';
          
          document.querySelectorAll('.cliente-input').forEach(input => {
            input.classList.add('autollenado');
          });
          
          deshabilitarInputsCliente();
          if (btnRegistrarCliente) btnRegistrarCliente.disabled = true;
          mostrarToastExito('El RFC ya está registrado. Los datos han sido cargados automáticamente.', 'error');
        } else {
          habilitarInputsCliente();
          if (btnRegistrarCliente) btnRegistrarCliente.disabled = false;
          mostrarToastExito('RFC válido. Puede continuar con el registro.', 'success');
        }
      } catch (error) {
        console.error('Error:', error);
        mostrarToastExito('Error al validar RFC', 'error');
      }
    });
  }
});
