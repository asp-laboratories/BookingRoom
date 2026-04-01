document.addEventListener('DOMContentLoaded', function() {
  // === PAQUETES ===
  let paqueteServicioIndex = 1;
  let paqueteEquipamientoIndex = 1;

  window.anadirPaqueteServicio = function() {
    paqueteServicioIndex++;
    const container = document.getElementById('paquete-servicios-list');
    const primerSelectTipo = document.querySelector('#paquete-servicios-list .paquete-servicio-tipo');
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : '';
    
    const html = `
      <div class="paquetes-servicio-pair" data-index="${paqueteServicioIndex}">
        <div class="paquetes-campo">
          <label class="paquetes-label">Tipo de servicio</label>
          <select class="paquetes-input paquete-servicio-tipo" name="servicio_tipo_${paqueteServicioIndex}">
            ${opcionesTipo}
          </select>
        </div>
        <div class="paquetes-campo">
          <label class="paquetes-label">Seleccionar Servicio</label>
          <select class="paquetes-input paquete-servicio-select" name="servicio_${paqueteServicioIndex}" disabled>
            <option value="">-- Selecciona un tipo primero --</option>
          </select>
        </div>
      </div>
    `;
    container.insertAdjacentHTML('beforeend', html);
    agregarEventosPaqueteServicios();
  };

  window.anadirPaqueteEquipamiento = function() {
    paqueteEquipamientoIndex++;
    const container = document.getElementById('paquete-equipamientos-list');
    const primerSelectTipo = document.querySelector('#paquete-equipamientos-list .paquete-equipamiento-tipo');
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : '';
    
    const html = `
      <div class="paquetes-equipamiento-pair" data-index="${paqueteEquipamientoIndex}">
        <div class="paquetes-campo">
          <label class="paquetes-label">Tipo de equipamiento</label>
          <select class="paquetes-input paquete-equipamiento-tipo" name="equipamiento_tipo_${paqueteEquipamientoIndex}">
            ${opcionesTipo}
          </select>
        </div>
        <div class="paquetes-campo">
          <label class="paquetes-label">Seleccionar Equipo</label>
          <select class="paquetes-input paquete-equipamiento-select" name="equipamiento_${paqueteEquipamientoIndex}" disabled>
            <option value="">-- Selecciona un tipo primero --</option>
          </select>
        </div>
        <div class="paquetes-campo">
          <label class="paquetes-label">Cantidad</label>
          <input type="number" class="paquetes-input" name="equipamiento_cantidad_${paqueteEquipamientoIndex}" value="1" min="1">
        </div>
      </div>
    `;
    container.insertAdjacentHTML('beforeend', html);
    agregarEventosPaqueteEquipamientos();
  };

  window.quitarPaqueteItem = function(tipo) {
    const container = document.getElementById(tipo === 'servicios' ? 'paquete-servicios-list' : 'paquete-equipamientos-list');
    if (container && container.children.length > 1) {
      container.removeChild(container.lastChild);
    }
  };

  async function cargarPaqueteServiciosPorTipo(tipoSelect, servicioSelect) {
    const tipoId = tipoSelect.value;
    if (!tipoId) {
      servicioSelect.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
      servicioSelect.disabled = true;
      return;
    }
    
    try {
      const response = await fetch(`/reservacion/servicios-por-tipo/?tipo_id=${tipoId}`);
      const data = await response.json();
      
      const serviciosYaSeleccionados = Array.from(document.querySelectorAll('.paquete-servicio-select'))
        .filter(s => s !== servicioSelect).map(s => s.value).filter(v => v !== '');
      
      servicioSelect.innerHTML = '<option value="">-- Elige un servicio --</option>';
      
      if (data.servicios && data.servicios.length > 0) {
        data.servicios.forEach(servicio => {
          const option = document.createElement('option');
          option.value = servicio.id;
          option.textContent = `${servicio.nombre} - $${servicio.costo}`;
          option.dataset.costo = servicio.costo;
          
          if (serviciosYaSeleccionados.includes(String(servicio.id))) {
            option.disabled = true;
            option.textContent += ' (ya seleccionado)';
          }
          
          servicioSelect.appendChild(option);
        });
        servicioSelect.disabled = false;
      } else {
        servicioSelect.innerHTML = '<option value="">-- No hay servicios disponibles --</option>';
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  async function cargarPaqueteEquipamientoPorTipo(tipoSelect, equipamentoSelect) {
    const tipoId = tipoSelect.value;
    if (!tipoId) {
      equipamentoSelect.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
      equipamentoSelect.disabled = true;
      return;
    }
    
    try {
      const response = await fetch(`/reservacion/equipamiento-por-tipo/?tipo_id=${tipoId}`);
      const data = await response.json();
      
      const equiposYaSeleccionados = Array.from(document.querySelectorAll('.paquete-equipamiento-select'))
        .filter(s => s !== equipamentoSelect).map(s => s.value).filter(v => v !== '');
      
      equipamentoSelect.innerHTML = '<option value="">-- Elige un equipamento --</option>';
      
      if (data.equipamientos && data.equipamientos.length > 0) {
        data.equipamientos.forEach(equip => {
          const option = document.createElement('option');
          option.value = equip.id;
          option.textContent = `${equip.nombre} - $${equip.costo} (Stock: ${equip.stock})`;
          option.dataset.costo = equip.costo;
          option.dataset.stock = equip.stock;
          
          if (equiposYaSeleccionados.includes(String(equip.id))) {
            option.disabled = true;
            option.textContent += ' (ya seleccionado)';
          }
          
          equipamentoSelect.appendChild(option);
        });
        equipamentoSelect.disabled = false;
      } else {
        equipamentoSelect.innerHTML = '<option value="">-- No hay equipamentos disponibles --</option>';
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  window.actualizarOpcionesPaquete = function(claseSelect) {
    const selects = document.querySelectorAll('.' + claseSelect);
    if (selects.length === 0) return;
    
    const valoresSeleccionados = Array.from(selects).map(s => s.value).filter(v => v !== '');
    selects.forEach(function(select) {
      Array.from(select.options).forEach(function(option) {
        if (valoresSeleccionados.includes(option.value) && option.value !== select.value) {
          option.disabled = true;
        } else if (!option.disabled) {
          option.disabled = false;
        }
      });
    });
  };

  function agregarEventosPaqueteServicios() {
    document.querySelectorAll('.paquete-servicio-tipo').forEach(function(select) {
      select.addEventListener('change', function() {
        const pair = this.closest('.paquetes-servicio-pair');
        const servicioSelect = pair.querySelector('.paquete-servicio-select');
        cargarPaqueteServiciosPorTipo(this, servicioSelect);
      });
    });
    
    document.querySelectorAll('.paquete-servicio-select').forEach(function(select) {
      select.addEventListener('change', function() {
        actualizarOpcionesPaquete('paquete-servicio-select');
      });
    });
  }

  function agregarEventosPaqueteEquipamientos() {
    document.querySelectorAll('.paquete-equipamiento-tipo').forEach(function(select) {
      select.addEventListener('change', function() {
        const pair = this.closest('.paquetes-equipamiento-pair');
        const equipamentoSelect = pair.querySelector('.paquete-equipamiento-select');
        cargarPaqueteEquipamientoPorTipo(this, equipamentoSelect);
      });
    });
    
    document.querySelectorAll('.paquete-equipamiento-select').forEach(function(select) {
      select.addEventListener('change', function() {
        actualizarOpcionesPaquete('paquete-equipamiento-select');
      });
    });
  }

  // Calcular total
  window.calcularPaqueteTotal = function() {
    const subtotal = parseFloat(document.getElementById('paquete-subtotal').value) || 0;
    const iva = parseFloat(document.getElementById('paquete-iva').value) || 0;
    const total = subtotal + (subtotal * iva / 100);
    const totalInput = document.getElementById('paquete-total');
    if (totalInput) totalInput.value = total.toFixed(2);
  };

  // Guardar paquete
  window.guardarPaquete = function() {
    const nombre = document.getElementById('paquete-nombre').value;
    if (!nombre.trim()) {
      alert('Por favor ingresa un nombre para el paquete');
      return;
    }
    alert('Funcionalidad de guardado en desarrollo');
  };

  // Inicializar eventos
  agregarEventosPaqueteServicios();
  agregarEventosPaqueteEquipamientos();

  // Eventos para cálculo de total
  const subtotalInput = document.getElementById('paquete-subtotal');
  const ivaInput = document.getElementById('paquete-iva');
  if (subtotalInput) subtotalInput.addEventListener('input', calcularPaqueteTotal);
  if (ivaInput) ivaInput.addEventListener('input', calcularPaqueteTotal);
});