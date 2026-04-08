document.addEventListener('DOMContentLoaded', function() {
  let paqueteServicioIndex = 1;
  let paqueteEquipamientoIndex = 1;
  let paqueteMobiliarioIndex = 1;

  window.openPaquetesTab = function(tabName, btnElement) {
    document.querySelectorAll('.paquetes-tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.paquetes-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('paquetes-tab-' + tabName).classList.add('active');
    if (btnElement) {
      btnElement.classList.add('active');
    }
  };

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
    const container = document.getElementById('paquete-equipamiento-list');
    const primerSelectTipo = document.querySelector('#paquete-equipamiento-list .paquete-equipamiento-tipo');
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : '';
    
    const html = `
      <div class="paquetes-servicio-pair" data-index="${paqueteEquipamientoIndex}">
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

  window.anadirPaqueteMobiliario = function() {
    paqueteMobiliarioIndex++;
    const container = document.getElementById('paquete-mobiliario-list');
    const primerSelectTipo = document.querySelector('#paquete-mobiliario-list .paquete-mobiliario-tipo');
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : '';
    
    const html = `
      <div class="paquetes-servicio-pair" data-index="${paqueteMobiliarioIndex}">
        <div class="paquetes-campo">
          <label class="paquetes-label">Tipo de mobiliario</label>
          <select class="paquetes-input paquete-mobiliario-tipo" name="mobiliario_tipo_${paqueteMobiliarioIndex}">
            ${opcionesTipo}
          </select>
        </div>
        <div class="paquetes-campo">
          <label class="paquetes-label">Seleccionar Mobiliario</label>
          <select class="paquetes-input paquete-mobiliario-select" name="mobiliario_${paqueteMobiliarioIndex}" disabled>
            <option value="">-- Selecciona un tipo primero --</option>
          </select>
        </div>
        <div class="paquetes-campo">
          <label class="paquetes-label">Cantidad</label>
          <input type="number" class="paquetes-input" name="mobiliario_cantidad_${paqueteMobiliarioIndex}" value="1" min="1">
        </div>
      </div>
    `;
    container.insertAdjacentHTML('beforeend', html);
    agregarEventosPaqueteMobiliarios();
  };

  window.quitarPaqueteSelect = function(tipo) {
    let container;
    if (tipo === 'servicios') {
      container = document.getElementById('paquete-servicios-list');
    } else if (tipo === 'equipamientos') {
      container = document.getElementById('paquete-equipamiento-list');
    } else if (tipo === 'mobiliarios') {
      container = document.getElementById('paquete-mobiliario-list');
    }
    
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

  async function cargarPaqueteMobiliarioPorTipo(tipoSelect, mobiliarioSelect) {
    const tipoId = tipoSelect.value;
    if (!tipoId) {
      mobiliarioSelect.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
      mobiliarioSelect.disabled = true;
      return;
    }
    
    try {
      const response = await fetch(`/reservacion/mobiliarios-tipo/?tipo_id=${tipoId}`);
      const data = await response.json();
      
      const mobiliariosYaSeleccionados = Array.from(document.querySelectorAll('.paquete-mobiliario-select'))
        .filter(s => s !== mobiliarioSelect).map(s => s.value).filter(v => v !== '');
      
      mobiliarioSelect.innerHTML = '<option value="">-- Elige un mobiliario --</option>';
      
      if (data.mobiliarios && data.mobiliarios.length > 0) {
        data.mobiliarios.forEach(mob => {
          const option = document.createElement('option');
          option.value = mob.id;
          option.textContent = `${mob.nombre} - $${mob.costo} (Stock: ${mob.stock})`;
          option.dataset.costo = mob.costo;
          option.dataset.stock = mob.stock;
          
          if (mobiliariosYaSeleccionados.includes(String(mob.id))) {
            option.disabled = true;
            option.textContent += ' (ya seleccionado)';
          }
          
          mobiliarioSelect.appendChild(option);
        });
        mobiliarioSelect.disabled = false;
      } else {
        mobiliarioSelect.innerHTML = '<option value="">-- No hay mobiliarios disponibles --</option>';
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
        const pair = this.closest('.paquetes-servicio-pair');
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

  function agregarEventosPaqueteMobiliarios() {
    document.querySelectorAll('.paquete-mobiliario-tipo').forEach(function(select) {
      select.addEventListener('change', function() {
        const pair = this.closest('.paquetes-servicio-pair');
        const mobiliarioSelect = pair.querySelector('.paquete-mobiliario-select');
        cargarPaqueteMobiliarioPorTipo(this, mobiliarioSelect);
      });
    });
    
    document.querySelectorAll('.paquete-mobiliario-select').forEach(function(select) {
      select.addEventListener('change', function() {
        actualizarOpcionesPaquete('paquete-mobiliario-select');
      });
    });
  }

  window.calcularPaqueteTotal = function() {
    let subtotal = 0;
    
    document.querySelectorAll('.paquete-servicio-select').forEach(function(select) {
      if (select.value) {
        const option = select.options[select.selectedIndex];
        if (option && option.dataset.costo) {
          subtotal += parseFloat(option.dataset.costo);
        }
      }
    });
    
    document.querySelectorAll('.paquete-equipamiento-select').forEach(function(select) {
      if (select.value) {
        const option = select.options[select.selectedIndex];
        const pair = select.closest('.paquetes-servicio-pair');
        const cantidadInput = pair.querySelector('input[name^="equipamiento_cantidad_"]');
        const cantidad = cantidadInput ? parseInt(cantidadInput.value) || 1 : 1;
        
        if (option && option.dataset.costo) {
          subtotal += parseFloat(option.dataset.costo) * cantidad;
        }
      }
    });
    
    document.querySelectorAll('.paquete-mobiliario-select').forEach(function(select) {
      if (select.value) {
        const option = select.options[select.selectedIndex];
        const pair = select.closest('.paquetes-servicio-pair');
        const cantidadInput = pair.querySelector('input[name^="mobiliario_cantidad_"]');
        const cantidad = cantidadInput ? parseInt(cantidadInput.value) || 1 : 1;
        
        if (option && option.dataset.costo) {
          subtotal += parseFloat(option.dataset.costo) * cantidad;
        }
      }
    });
    
    const salonSelect = document.getElementById('paquete-salon-select');
    if (salonSelect && salonSelect.dataset.costo) {
      subtotal += parseFloat(salonSelect.dataset.costo);
    }
    
    const subtotalInput = document.getElementById('paquete-subtotal');
    const ivaInput = document.getElementById('paquete-iva');
    const totalInput = document.getElementById('paquete-total');
    
    if (subtotalInput) subtotalInput.value = subtotal.toFixed(2);
    
    if (ivaInput && totalInput) {
      const iva = parseFloat(ivaInput.value) || 0;
      const total = subtotal + (subtotal * iva / 100);
      totalInput.value = total.toFixed(2);
    }
  };

  window.guardarPaquete = function() {
    const nombre = document.getElementById('paquete-nombre').value;
    const salonSelect = document.getElementById('paquete-salon-select');
    const montajeSelect = document.getElementById('paquete-montaje-select');
    
    if (!nombre.trim()) {
      alert('Por favor ingresa un nombre para el paquete');
      return;
    }
    
    if (!salonSelect.value) {
      alert('Por favor selecciona un salon');
      return;
    }
    
    if (!montajeSelect.value) {
      alert('Por favor selecciona un montaje');
      return;
    }
    
    const servicios = [];
    document.querySelectorAll('.paquete-servicio-select').forEach(function(select) {
      if (select.value) {
        servicios.push(select.value);
      }
    });
    
    const equipamiento = [];
    document.querySelectorAll('.paquete-equipamiento-select').forEach(function(select) {
      if (select.value) {
        const pair = select.closest('.paquetes-servicio-pair');
        const cantidadInput = pair.querySelector('input[name^="equipamiento_cantidad_"]');
        equipamiento.push({
          id: select.value,
          cantidad: cantidadInput ? cantidadInput.value : 1
        });
      }
    });
    
    const mobiliario = [];
    document.querySelectorAll('.paquete-mobiliario-select').forEach(function(select) {
      if (select.value) {
        const pair = select.closest('.paquetes-servicio-pair');
        const cantidadInput = pair.querySelector('input[name^="mobiliario_cantidad_"]');
        mobiliario.push({
          id: select.value,
          cantidad: cantidadInput ? cantidadInput.value : 1
        });
      }
    });
    
    const formData = new FormData();
    formData.append('nombre_paquete', nombre);
    formData.append('salon_id', salonSelect.value);
    formData.append('montaje_id', montajeSelect.value);
    formData.append('subtotal', document.getElementById('paquete-subtotal').value || 0);
    formData.append('iva', document.getElementById('paquete-iva').value || 16);
    formData.append('total', document.getElementById('paquete-total').value || 0);
    
    servicios.forEach(s => formData.append('servicios[]', s));
    
    equipamiento.forEach((eq, index) => {
      formData.append(`equipamiento_${index + 1}_id`, eq.id);
      formData.append(`equipamiento_${index + 1}_cantidad`, eq.cantidad);
    });
    
    mobiliario.forEach((mob, index) => {
      formData.append(`mobiliario_${index + 1}_id`, mob.id);
      formData.append(`mobiliario_${index + 1}_cantidad`, mob.cantidad);
    });
    
    fetch('/administracion/paquetes/crear/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Paquete creado correctamente');
        location.reload();
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al crear el paquete');
    });
  };

  window.verPaquete = function(pk) {
    fetch(`/administracion/paquetes/${pk}/detalle/`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const paquete = data.paquete;
        let html = `
          <div class="detalle-seccion">
            <h4>Informacion General</h4>
            <p><strong>Nombre:</strong> ${paquete.nombre_paquete || 'N/A'}</p>
            <p><strong>Salon:</strong> ${paquete.salon_nombre || 'N/A'}</p>
            <p><strong>Montaje:</strong> ${paquete.montaje_nombre || 'N/A'}</p>
            <p><strong>Subtotal:</strong> $${paquete.subtotal || '0.00'}</p>
            <p><strong>IVA:</strong> ${paquete.iva || '16'}%</p>
            <p><strong>Total:</strong> $${paquete.total || '0.00'}</p>
          </div>
        `;
        
        if (data.servicios && data.servicios.length > 0) {
          html += `<div class="detalle-seccion"><h4>Servicios (${data.servicios.length})</h4><ul class="detalle-lista">`;
          data.servicios.forEach(s => {
            html += `<li>${s.servicio__nombre} - $${s.servicio__costo}</li>`;
          });
          html += `</ul></div>`;
        }
        
        if (data.equipamiento && data.equipamiento.length > 0) {
          html += `<div class="detalle-seccion"><h4>Equipamiento (${data.equipamiento.length})</h4><ul class="detalle-lista">`;
          data.equipamiento.forEach(e => {
            html += `<li>${e.equipamiento__nombre} (Cant: ${e.cantidad}) - $${e.equipamiento__costo}</li>`;
          });
          html += `</ul></div>`;
        }
        
        if (data.mobiliario && data.mobiliario.length > 0) {
          html += `<div class="detalle-seccion"><h4>Mobiliario (${data.mobiliario.length})</h4><ul class="detalle-lista">`;
          data.mobiliario.forEach(m => {
            html += `<li>${m.mobiliario__nombre} (Cant: ${m.cantidad}) - $${m.mobiliario__costo}</li>`;
          });
          html += `</ul></div>`;
        }
        
        document.getElementById('modal-paquete-titulo').textContent = paquete.nombre_paquete || 'Detalle del Paquete';
        document.getElementById('modal-paquete-body').innerHTML = html;
        document.getElementById('modal-ver-paquete').showModal();
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al cargar los detalles del paquete');
    });
  };

  window.editarPaquete = function(pk) {
    fetch(`/administracion/paquetes/${pk}/detalle/`)
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        paqueteEditandoId = pk;
        const paquete = data.paquete;
        
        document.getElementById('editar-nombre').value = paquete.nombre_paquete || '';
        document.getElementById('editar-subtotal').value = paquete.subtotal || '0';
        document.getElementById('editar-iva').value = paquete.iva || '16';
        document.getElementById('editar-total').value = paquete.total || '0';
        
        const salonSelect = document.getElementById('editar-salon');
        salonSelect.value = paquete.salon_id || '';
        
        if (paquete.salon_id) {
          cargarMontajesEditar(paquete.salon_id, paquete.montaje_id);
        }
        
        document.getElementById('modal-editar-paquete').showModal();
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al cargar el paquete');
    });
  };

  async function cargarMontajesEditar(salonId, selectedMontajeId) {
    const montajeSelect = document.getElementById('editar-montaje');
    
    if (!salonId) {
      montajeSelect.innerHTML = '<option value="">-- Selecciona un salon primero --</option>';
      montajeSelect.disabled = true;
      return;
    }
    
    try {
      const response = await fetch(`/reservacion/montajes-salon/?salon_id=${salonId}`);
      const data = await response.json();
      
      montajeSelect.innerHTML = '<option value="">-- Selecciona un montaje --</option>';
      
      if (data.montajes && data.montajes.length > 0) {
        data.montajes.forEach(montaje => {
          const option = document.createElement('option');
          option.value = montage.id;
          option.textContent = `${montaje.nombre} (Capacidad: ${montaje.capacidadIdeal})`;
          if (selectedMontajeId && montage.id == selectedMontajeId) {
            option.selected = true;
          }
          montajeSelect.appendChild(option);
        });
        montajeSelect.disabled = false;
      } else {
        montajeSelect.innerHTML = '<option value="">-- No hay montajes disponibles --</option>';
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  document.getElementById('editar-salon').addEventListener('change', function() {
    cargarMontajesEditar(this.value, null);
  });

  document.getElementById('editar-iva').addEventListener('input', function() {
    calcularTotalEditar();
  });

  document.getElementById('editar-subtotal').addEventListener('input', function() {
    calcularTotalEditar();
  });

  function calcularTotalEditar() {
    const subtotal = parseFloat(document.getElementById('editar-subtotal').value) || 0;
    const iva = parseFloat(document.getElementById('editar-iva').value) || 0;
    const total = subtotal + (subtotal * iva / 100);
    document.getElementById('editar-total').value = total.toFixed(2);
  }

  window.guardarEdicionPaquete = function() {
    if (!paqueteEditandoId) {
      alert('Error: No se ha seleccionado un paquete para editar');
      return;
    }
    
    const nombre = document.getElementById('editar-nombre').value.trim();
    const salonId = document.getElementById('editar-salon').value;
    const montajeId = document.getElementById('editar-montaje').value;
    const subtotal = document.getElementById('editar-subtotal').value;
    const iva = document.getElementById('editar-iva').value;
    const total = document.getElementById('editar-total').value;
    
    if (!nombre) {
      alert('Por favor ingresa un nombre para el paquete');
      return;
    }
    
    const formData = new FormData();
    formData.append('nombre_paquete', nombre);
    formData.append('salon_id', salonId);
    formData.append('montaje_id', montajeId);
    formData.append('subtotal', subtotal);
    formData.append('iva', iva);
    formData.append('total', total);
    
    fetch(`/administracion/paquetes/${paqueteEditandoId}/editar/`, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Paquete actualizado correctamente');
        cerrarModalEditar();
        location.reload();
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al actualizar el paquete');
    });
  };

  window.cerrarModalEditar = function() {
    document.getElementById('modal-editar-paquete').close();
    paqueteEditandoId = null;
  };

  window.duplicarPaquete = function(pk) {
    if (!confirm('Deseas duplicar este paquete?')) return;
    
    fetch(`/administracion/paquetes/${pk}/duplicar/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Paquete duplicado correctamente');
        location.reload();
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al duplicar el paquete');
    });
  };

  window.eliminarPaquete = function(pk) {
    if (!confirm('Estas seguro de que deseas eliminar este paquete? Esta accion no se puede deshacer.')) return;
    
    fetch(`/administracion/paquetes/${pk}/eliminar/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Paquete eliminado correctamente');
        location.reload();
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error al eliminar el paquete');
    });
  };

  document.getElementById('paquete-salon-select').addEventListener('change', async function() {
    const salonId = this.value;
    const montajeSelect = document.getElementById('paquete-montaje-select');
    
    if (!salonId) {
      montajeSelect.innerHTML = '<option value="">-- Selecciona un salon primero --</option>';
      montajeSelect.disabled = true;
      return;
    }
    
    try {
      const response = await fetch(`/reservacion/montajes-salon/?salon_id=${salonId}`);
      const data = await response.json();
      
      this.dataset.costo = data.salon ? data.salon.costo : 0;
      
      montajeSelect.innerHTML = '<option value="">-- Selecciona un montaje --</option>';
      
      if (data.montajes && data.montajes.length > 0) {
        data.montajes.forEach(montaje => {
          const option = document.createElement('option');
          option.value = montage.id;
          option.textContent = `${montaje.nombre} (Capacidad: ${montaje.capacidadIdeal})`;
          montajeSelect.appendChild(option);
        });
        montajeSelect.disabled = false;
      } else {
        montajeSelect.innerHTML = '<option value="">-- No hay montajes disponibles --</option>';
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });

  agregarEventosPaqueteServicios();
  agregarEventosPaqueteEquipamientos();
  agregarEventosPaqueteMobiliarios();

  const subtotalInput = document.getElementById('paquete-subtotal');
  const ivaInput = document.getElementById('paquete-iva');
  if (subtotalInput) subtotalInput.addEventListener('input', calcularPaqueteTotal);
  if (ivaInput) ivaInput.addEventListener('input', calcularPaqueteTotal);
});

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
