// ========================================
// GESTIÓN DE SELECTS DINÁMICOS
// Servicios, Equipamiento, Mobiliario
// ========================================

let contadorServicios = 1;
let contadorEquipamientos = 1;
let contadorMobiliarios = 1;

// ========================================
// AÑADIR NUEVOS SELECTS
// ========================================

function añadirSelect() {
  contadorServicios++;
  const contenedor = document.getElementById("servicios-selects");
  const primerSelectTipo = document.querySelector(".servicio-tipo");
  const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";

  const nuevoPair = document.createElement("div");
  nuevoPair.className = "servicio-pair";
  nuevoPair.setAttribute("data-index", contadorServicios);
  nuevoPair.innerHTML = `
    <div class="reservacion-campo">
      <label class="reservacion-label">Tipo de servicio</label>
      <select class="reservacion-input servicio-tipo" name="servicio_tipo_${contadorServicios}">
        ${opcionesTipo}
      </select>
    </div>
    <div class="reservacion-campo">
      <label class="reservacion-label">Seleccionar Servicio</label>
      <select class="reservacion-input servicio-select" name="servicio_${contadorServicios}" disabled>
        <option value="">-- Selecciona un tipo primero --</option>
      </select>
    </div>
  `;
  contenedor.appendChild(nuevoPair);

  // Event listeners para el nuevo par
  nuevoPair.querySelector(".servicio-tipo").addEventListener("change", function () {
    cargarServiciosPorTipo(this, nuevoPair.querySelector(".servicio-select"));
  });
  nuevoPair.querySelector(".servicio-select").addEventListener("change", function () {
    actualizarOpcionesSelect("servicio-select");
  });
}

function añadirEquipamiento() {
  contadorEquipamientos++;
  const contenedor = document.getElementById("equipamientos-selects");
  const primerSelectTipo = document.querySelector(".equipamiento-tipo");
  const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";

  const nuevoPair = document.createElement("div");
  nuevoPair.className = "equipo-pair";
  nuevoPair.setAttribute("data-index", contadorEquipamientos);
  nuevoPair.innerHTML = `
    <div class="reservacion-campo">
      <label class="reservacion-label">Tipo de equipamiento</label>
      <select class="reservacion-input equipamiento-tipo" name="equipamiento_tipo_${contadorEquipamientos}">
        ${opcionesTipo}
      </select>
    </div>
    <div class="reservacion-campo">
      <label class="reservacion-label">Seleccionar Equipo</label>
      <select class="reservacion-input equipamiento-select" name="equipamiento_${contadorEquipamientos}" disabled>
        <option value="">-- Selecciona un tipo primero --</option>
      </select>
    </div>
    <div class="reservacion-campo">
      <label class="reservacion-label">Cantidad</label>
      <input type="number" class="reservacion-input" name="equipamiento_cantidad_${contadorEquipamientos}" value="1" min="1" />
    </div>
  `;
  contenedor.appendChild(nuevoPair);

  // Event listeners para el nuevo par
  nuevoPair.querySelector(".equipamiento-tipo").addEventListener("change", function () {
    cargarEquipamientoPorTipo(this, nuevoPair.querySelector(".equipamiento-select"));
  });
  nuevoPair.querySelector(".equipamiento-select").addEventListener("change", function () {
    actualizarOpcionesSelect("equipamiento-select");
  });
}

function anadirMobiliario() {
  contadorMobiliarios++;
  const contenedor = document.getElementById("mobiliarios-selects");
  const primerSelectTipo = document.querySelector(".mobiliario-tipo");
  const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";
  const montajeSeleccionado = document.getElementById("select-montaje") && document.getElementById("select-montaje").value;

  const nuevoPair = document.createElement("div");
  nuevoPair.className = "mobil-pair";
  nuevoPair.setAttribute("data-index", contadorMobiliarios);
  nuevoPair.innerHTML = `
    <div class="reservacion-campo">
      <label class="reservacion-label">Tipo de mobiliario</label>
      <select class="reservacion-input mobiliario-tipo" name="mobiliario_tipo_${contadorMobiliarios}" ${!montajeSeleccionado ? 'disabled' : ''}>
        ${opcionesTipo}
      </select>
    </div>
    <div class="reservacion-campo">
      <label class="reservacion-label">Seleccionar Mobiliario</label>
      <select class="reservacion-input mobiliario-select" name="mobiliario_${contadorMobiliarios}" disabled>
        <option value="">-- Selecciona un tipo primero --</option>
      </select>
    </div>
    <div class="reservacion-campo">
      <label class="reservacion-label">Cantidad</label>
      <input type="number" class="reservacion-input" name="mobiliario_cantidad_${contadorMobiliarios}" value="1" min="1" />
    </div>
  `;
  contenedor.appendChild(nuevoPair);

  // Event listeners para el nuevo par
  nuevoPair.querySelector(".mobiliario-tipo").addEventListener("change", function () {
    cargarMobiliariosPorTipo(this, nuevoPair.querySelector(".mobiliario-select"));
  });
}

function quitarSelect(tipo) {
  let contenedor, selector;
  if (tipo === "servicios") {
    contenedor = document.getElementById("servicios-selects");
    selector = ".servicio-pair";
  } else if (tipo === "equipamientos") {
    contenedor = document.getElementById("equipamientos-selects");
    selector = ".equipo-pair";
  } else if (tipo === "mobiliarios") {
    contenedor = document.getElementById("mobiliarios-selects");
    selector = ".mobil-pair";
  }

  if (contenedor) {
    const items = contenedor.querySelectorAll(selector);
    if (items.length > 1) {
      contenedor.removeChild(items[items.length - 1]);
    } else {
      mostrarToastExito("Debe mantener al menos uno", "warning");
    }
  }
}

// ========================================
// CARGAR DATOS POR TIPO (AJAX)
// ========================================

async function cargarServiciosPorTipo(tipoSelect, servicioSelect) {
  const tipoId = tipoSelect.value;

  if (!tipoId) {
    servicioSelect.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
    servicioSelect.disabled = true;
    return;
  }

  try {
    const response = await fetch(`/reservacion/servicios-por-tipo/?tipo_id=${tipoId}`);
    const data = await response.json();

    const yaSeleccionados = obtenerYaSeleccionados(".servicio-select", servicioSelect);
    servicioSelect.innerHTML = '<option value="">-- Elige un servicio --</option>';

    if (data.servicios && data.servicios.length > 0) {
      data.servicios.forEach(servicio => {
        const option = document.createElement("option");
        option.value = servicio.id;
        option.textContent = `${servicio.nombre} - $${servicio.costo}`;
        option.dataset.costo = servicio.costo;

        if (yaSeleccionados.includes(String(servicio.id))) {
          option.disabled = true;
          option.textContent += " (ya seleccionado)";
        }
        servicioSelect.appendChild(option);
      });
      servicioSelect.disabled = false;
    } else {
      servicioSelect.innerHTML = '<option value="">-- No hay servicios disponibles --</option>';
    }
  } catch (error) {
    console.error("Error cargando servicios:", error);
    mostrarToastExito("Error al cargar servicios", "error");
  }
}

async function cargarEquipamientoPorTipo(tipoSelect, equipamientoSelect) {
  const tipoId = tipoSelect.value;

  if (!tipoId) {
    equipamientoSelect.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
    equipamientoSelect.disabled = true;
    return;
  }

  try {
    const response = await fetch(`/reservacion/equipamiento-por-tipo/?tipo_id=${tipoId}`);
    const data = await response.json();

    const yaSeleccionados = obtenerYaSeleccionados(".equipamiento-select", equipamientoSelect);
    equipamientoSelect.innerHTML = '<option value="">-- Elige un equipo --</option>';

    if (data.equipamientos && data.equipamientos.length > 0) {
      data.equipamientos.forEach(equip => {
        const option = document.createElement("option");
        option.value = equip.id;
        option.textContent = `${equip.nombre} - $${equip.costo} (Stock: ${equip.stock})`;
        option.dataset.costo = equip.costo;
        option.dataset.stock = equip.stock;

        if (yaSeleccionados.includes(String(equip.id))) {
          option.disabled = true;
          option.textContent += " (ya seleccionado)";
        }
        equipamientoSelect.appendChild(option);
      });
      equipamientoSelect.disabled = false;
    } else {
      equipamientoSelect.innerHTML = '<option value="">-- No hay equipos disponibles --</option>';
    }
  } catch (error) {
    console.error("Error cargando equipamiento:", error);
    mostrarToastExito("Error al cargar equipamiento", "error");
  }
}

// funcion pa poner montajes por salon (en duda aun pero anadido por si acaso)
async function cargarMontajesSalon(salon) {
  const montajeElegido = document.getElementById("select-montaje");

  document.querySelectorAll(".mobiliario-tipo").forEach((s) => {
    s.disabled = true;
    s.value = "";
  });
  document.querySelectorAll(".mobiliario-select").forEach((s) => {
    s.disabled = true;
    s.innerHTML = '<option value="">-- Seleccion un tipo primero --</option>';
  });

  if (!salon) {
    montajeElegido.innerHTML =
      '<option value="">-- Selecciona un salon primero --</option>';
    montajeElegido.disabled = true;
    return;
  }

  try {
    const repuesta = await fetch(
      `/reservacion/montajes-salon/?salon_id=${salon}`,
    );
    const datos = await repuesta.json();

    montajeElegido.innerHTML =
      '<option value="">-- Selecciona un montaje --</option>';
    montajeElegido.disabled = false;

    if (datos.montajes && datos.montajes.length > 0) {
      datos.montajes.forEach((montaje) => {
        const option = document.createElement("option");
        option.value = montaje.id;  // Usar tipo_montaje_id, no montaje.id
        option.textContent = `${montaje.nombre} (Capacidad: ${montaje.capacidadIdeal || 'N/A'})`;
        option.dataset.costo = montaje.costo || 0; // Guardar costo para calculo dinamico
        option.dataset.montajeId = montaje.id; // Guardar ID del montaje existente para referencia
        montajeElegido.appendChild(option);
      });
    } else {
      montajeElegido.innerHTML =
        '<option value="">-- No se encontraron montajes --</option>';
    }

    // Mostrar información del salón seleccionado en la consola
    if (datos.salon) {
      console.log(`Salón: ${datos.salon.nombre} - Costo: $${datos.salon.costo} - Capacidad: ${datos.salon.capacidad}`);
    }
  } catch (error) {
    console.error("Error al cargar los montajes", error);
    mostrarToastExito("Error al cargar montajes", "error");
  }

  montajeElegido.addEventListener(
    "change",
    function () {
      const mobiliariosBloqueados =
        document.querySelectorAll(".mobiliario-tipo");
      if (this.value) {
        mobiliariosBloqueados.forEach((s) => (s.disabled = false));
      } else {
        mobiliariosBloqueados.forEach((s) => {
          s.disabled = true;
          s.value = "";
        });
      }
    },
    { once: true },
  );
}

async function cargarMobiliariosPorTipo(tipo, mobiliarioSelect) {
  const tipoId = tipo.value;

  if (!tipoId) {
    mobiliarioSelect.innerHTML = '<option value="">-- Selecciona un tipo primero --</option>';
    mobiliarioSelect.disabled = true;
    return;
  }

  try {
    const response = await fetch(`/reservacion/mobiliarios-tipo/?tipo_id=${tipoId}`);
    const data = await response.json();

    const yaSeleccionados = obtenerYaSeleccionados(".mobiliario-select", mobiliarioSelect);
    mobiliarioSelect.innerHTML = '<option value="">-- Elige un mobiliario --</option>';

    if (data.mobiliarios && data.mobiliarios.length > 0) {
      data.mobiliarios.forEach(mobiliario => {
        const option = document.createElement("option");
        option.value = mobiliario.id;
        option.textContent = `${mobiliario.nombre} - $${mobiliario.costo} (Stock: ${mobiliario.stock})`;
        option.dataset.costo = mobiliario.costo;

        if (yaSeleccionados.includes(String(mobiliario.id))) {
          option.disabled = true;
          option.textContent += " (ya seleccionado)";
        }
        mobiliarioSelect.appendChild(option);
      });
      mobiliarioSelect.disabled = false;
    } else {
      mobiliarioSelect.innerHTML = '<option value="">-- No hay mobiliarios disponibles --</option>';
    }
  } catch (error) {
    console.error("Error cargando mobiliarios:", error);
    mostrarToastExito("Error al cargar mobiliarios", "error");
  }
}

// ========================================
// UTILIDADES
// ========================================

function obtenerYaSeleccionados(selector, excepto) {
  return Array.from(document.querySelectorAll(selector))
    .filter(s => s !== excepto)
    .map(s => s.value)
    .filter(v => v !== "");
}

function actualizarOpcionesSelect(claseSelect) {
  const selects = document.querySelectorAll("." + claseSelect);
  const valoresSeleccionados = Array.from(selects).map(s => s.value).filter(v => v !== "");

  selects.forEach(select => {
    Array.from(select.options).forEach(option => {
      option.disabled = valoresSeleccionados.includes(option.value) && option.value !== select.value;
    });
  });
}

// ========================================
// EVENT LISTENERS GLOBALES (DOMContentLoaded)
// ========================================
document.addEventListener("DOMContentLoaded", function () {

  // Servicios - primer par
  const primerServicioTipo = document.querySelector(".servicio-tipo");
  const primerServicioSelect = document.querySelector(".servicio-select");
  if (primerServicioTipo && primerServicioSelect) {
    primerServicioTipo.addEventListener("change", function () {
      cargarServiciosPorTipo(this, this.closest(".servicio-pair").querySelector(".servicio-select"));
    });
    primerServicioSelect.addEventListener("change", function () {
      actualizarOpcionesSelect("servicio-select");
    });
  }

  // Equipamiento - primer par
  const primerEquipoTipo = document.querySelector(".equipamiento-tipo");
  const primerEquipoSelect = document.querySelector(".equipamiento-select");
  if (primerEquipoTipo && primerEquipoSelect) {
    primerEquipoTipo.addEventListener("change", function () {
      cargarEquipamientoPorTipo(this, this.closest(".equipo-pair").querySelector(".equipamiento-select"));
    });
    primerEquipoSelect.addEventListener("change", function () {
      actualizarOpcionesSelect("equipamiento-select");
    });
  }

  // Mobiliario - primer par
  document.querySelectorAll(".mobiliario-tipo").forEach(select => {
    select.addEventListener("change", function () {
      cargarMobiliariosPorTipo(this, this.closest(".mobil-pair").querySelector(".mobiliario-select"));
    });
  });
});
