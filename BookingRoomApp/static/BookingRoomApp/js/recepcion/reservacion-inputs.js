 document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("reservacion-overlay");
    const abrir = document.querySelector(".expandir-solicitud");
    const cerrar = document.getElementById("reservacion-cerrar");

    abrir.addEventListener("click", (e) => {
      e.preventDefault();
      overlay.classList.add("mostrar");
    });

    cerrar.addEventListener("click", () => {
      overlay.classList.remove("mostrar");
    });

    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("mostrar");
      }
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && overlay.classList.contains("mostrar")) {
        overlay.classList.remove("mostrar");
      }
    });
  });

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

  const btnBuscarCliente = document.getElementById('btn-buscar-cliente');
  const buscarInput = document.getElementById('buscar-cliente-input');
  const clienteInputs = document.querySelectorAll('.cliente-input');

  function habilitarInputsCliente() {
    clienteInputs.forEach(input => {
      input.disabled = false;
    });
  }

  function deshabilitarInputsCliente() {
    clienteInputs.forEach(input => {
      input.disabled = true;
    });
  }

  function limpiarInputsCliente() {
    clienteInputs.forEach(input => {
      input.value = '';
    });
  }

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
          // Cliente encontrado - llenar datos
          document.getElementById('cliente-rfc').value = data.cliente.rfc || '';
          document.getElementById('cliente-nombre').value = data.cliente.nombre || '';
          document.getElementById('cliente-apellido-paterno').value = data.cliente.apellido_paterno || '';
          document.getElementById('cliente-apellido-materno').value = data.cliente.apellido_materno || '';
          document.getElementById('cliente-nombre-fiscal').value = data.cliente.nombre_fiscal || '';
          document.getElementById('cliente-colonia').value = data.cliente.colonia || '';
          document.getElementById('cliente-calle').value = data.cliente.calle || '';
          document.getElementById('cliente-numero').value = data.cliente.numero || '';
          
          // Agregar clase autollenado para fondo casi blanco
          document.querySelectorAll('.cliente-input').forEach(input => {
            input.classList.add('autollenado');
          });
          
          // Tipo de cliente
          if (data.cliente.tipo_cliente) {
            const tipoMoral = document.getElementById('tipo-moral');
            const tipoFisica = document.getElementById('tipo-fisica');
            if (data.cliente.tipo_cliente.toLowerCase().includes('moral')) {
              tipoMoral.checked = true;
            } else {
              tipoFisica.checked = true;
            }
          }
          
          deshabilitarInputsCliente();
          mostrarToastExito('Cliente encontrado', 'success');
        } else {
          // Cliente no encontrado - habilitar inputs para registro manual
          habilitarInputsCliente();
          limpiarInputsCliente();
          
          // Quitar clase autollenado
          document.querySelectorAll('.cliente-input').forEach(input => {
            input.classList.remove('autollenado');
          });
          
          document.getElementById('cliente-rfc').value = query;
          document.getElementById('cliente-rfc').disabled = false;
          
          const botonRegistrar = document.getElementById('btn-registrar-cliente');
          botonRegistrar.disabled = false;

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
        btnBuscarCliente.click();
      }
    });
  }

  // Validar RFC al registrar cliente
  const btnRegistrarCliente = document.getElementById('btn-registrar-cliente');
  if (btnRegistrarCliente) {
    btnRegistrarCliente.addEventListener('click', async function() {
      const rfcInput = document.getElementById('cliente-rfc');
      const rfcValue = rfcInput.value.trim();
      
      if (!rfcValue) {
        mostrarToastExito('Ingrese el RFC del cliente', 'warning');
        return;
      }

      try {
        const response = await fetch(`/reservacion/buscar-cliente/?q=${encodeURIComponent(rfcValue)}`);
        const data = await response.json();

        if (data.encontrado) {
          // RFC ya existe - llenar datos automáticamente y mostrar error
          document.getElementById('cliente-nombre').value = data.cliente.nombre || '';
          document.getElementById('cliente-apellido-paterno').value = data.cliente.apellido_paterno || '';
          document.getElementById('cliente-apellido-materno').value = data.cliente.apellido_materno || '';
          document.getElementById('cliente-nombre-fiscal').value = data.cliente.nombre_fiscal || '';
          document.getElementById('cliente-colonia').value = data.cliente.colonia || '';
          document.getElementById('cliente-calle').value = data.cliente.calle || '';
          document.getElementById('cliente-numero').value = data.cliente.numero || '';
          
          // Agregar clase autollenado
          document.querySelectorAll('.cliente-input').forEach(input => {
            input.classList.add('autollenado');
          });
          
          deshabilitarInputsCliente();
          mostrarToastExito('El RFC ya está registrado. Los datos han sido cargados automáticamente.', 'error');
        } else {
          // RFC no existe - proceder con registro
          mostrarToastExito('RFC válido. Puede continuar con el registro.', 'success');
          // Aquí agregarías la lógica para guardar el cliente
        }
      } catch (error) {
        console.error('Error:', error);
        mostrarToastExito('Error al validar RFC', 'error');
      }
    });
  }