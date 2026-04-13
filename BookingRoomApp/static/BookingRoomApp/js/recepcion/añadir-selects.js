let contadorServicios = 1;
let contadorEquipamientos = 1;
let contadorMobiliarios = 1;

function añadirSelect() {
  contadorServicios++;

  const contenedor = document.getElementById("servicios-selects");

  // Obtener tipos de servicio del primer select
  const primerSelectTipo = document.querySelector("#servicios select");
  const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";

  // Crear nuevo par de selects
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

  // Agregar event listener al nuevo select de tipo
  const nuevoTipoSelect = nuevoPair.querySelector(".servicio-tipo");
  nuevoTipoSelect.addEventListener("change", function () {
    cargarServiciosPorTipo(this, nuevoPair.querySelector(".servicio-select"));
  });

  // Agregar event listener al nuevo select de servicio
  const nuevoServicioSelect = nuevoPair.querySelector(".servicio-select");
  nuevoServicioSelect.addEventListener("change", function () {
    actualizarOpcionesSelect("servicio-select");
  });
}

function añadirEquipamiento() {
  contadorEquipamientos++;

  const contenedor = document.getElementById("equipamientos-selects");
  const primerSelectTipo = document.querySelector(
    "#equipamientos .reservacion-campo:first-child select",
  );
  const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";

  // Crear nuevo par de selects con cantidad
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

  // Agregar event listener al nuevo select de tipo
  const nuevoTipoSelect = nuevoPair.querySelector(".equipamiento-tipo");
  nuevoTipoSelect.addEventListener("change", function () {
    cargarEquipamientoPorTipo(
      this,
      nuevoPair.querySelector(".equipamiento-select"),
    );
  });

  // Agregar event listener al nuevo select de equipamento
  const nuevoEquipamentoSelect = nuevoPair.querySelector(
    ".equipamiento-select",
  );
  nuevoEquipamentoSelect.addEventListener("change", function () {
    actualizarOpcionesSelect("equipamiento-select");
  });
}

function anadirMobiliario() {
  contadorMobiliarios++;

  const contenedor = document.getElementById("mobiliarios-selects");
  const primerSelectTipo = document.querySelector(".mobiliario-tipo");
  const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";

  // Crear nuevo par de selects con cantidad
  const nuevoPair = document.createElement("div");
  nuevoPair.className = "mobil-pair";
  nuevoPair.setAttribute("data-index", contadorMobiliarios);
  nuevoPair.innerHTML = `<div class="reservacion-campo">
            <label class="reservacion-label">Tipo de mobiliario</label>
            <select class="reservacion-input mobiliario-tipo" name="mobiliario_tipo_${contadorMobiliarios}" 
            ${document.getElementById("select-montaje").value ? "" : "disabled"}>
                ${opcionesTipo}
            </select>
        </div>
        <div class="reservacion-campo">
            <label class="reservacion-label">Seleccionar mobiliario</label>
            <select class="reservacion-input mobiliario-select" name="mobiliario_${contadorMobiliarios}" disabled>
                <option value="">-- Selecciona un tipo primero --</option>
            </select>
        </div>
        <div class="reservacion-campo">
            <label class="reservacion-label">Cantidad</label>
            <input type="number" class="reservacion-input" name="mobiliario_cantidad_${contadorMobiliarios}" value="1" min="1" />
        </div>`;

  contenedor.appendChild(nuevoPair);

  // Agregar event listener al nuevo select de tipo
  const nuevoTipoSelect = nuevoPair.querySelector(".mobiliario-tipo");
  nuevoTipoSelect.addEventListener("change", function () {
    cargarMobiliariosPorTipo(
      this,
      nuevoPair.querySelector(".mobiliario-select"),
    );
  });

  // Agregar event listener al nuevo select de equipamento
  const nuevoMobiliarioSelect = nuevoPair.querySelector(".mobiliario-select");
  nuevoMobiliarioSelect.addEventListener("change", function () {
    actualizarOpcionesSelect("mobiliario-select");
  });
}

function quitarSelect(tipo) {
  let contenedor;
  let pair;
  if (tipo === "servicios") {
    contenedor = document.getElementById("servicios-selects");
    pair = ".servicio-pair";
  } else if (tipo === "equipamientos") {
    contenedor = document.getElementById("equipamientos-selects");
    pair = ".equipo-pair";
  } else if (tipo === "mobiliarios") {
    contenedor = document.getElementById("mobiliarios-selects");
    pair = ".mobil-pair";
  }

  if (contenedor) {
    const pairs = contenedor.querySelectorAll(pair);
    if (pairs.length > 1) {
      contenedor.removeChild(pairs[pairs.length - 1]);
    } else {
      mostrarToastExito("Debe mantener al menos uno", "warning");
    }
  }
}

// Cargar servicios por tipo
async function cargarServiciosPorTipo(tipoSelect, servicioSelect) {
  const tipoId = tipoSelect.value;

  if (!tipoId) {
    servicioSelect.innerHTML =
      '<option value="">-- Selecciona un tipo primero --</option>';
    servicioSelect.disabled = true;
    return;
  }

  try {
    const response = await fetch(
      `/reservacion/servicios-por-tipo/?tipo_id=${tipoId}`,
    );
    const data = await response.json();

    // Obtener servicios ya seleccionados en otros selects
    const serviciosYaSeleccionados = Array.from(
      document.querySelectorAll(".servicio-select"),
    )
      .filter((s) => s !== servicioSelect)
      .map((s) => s.value)
      .filter((v) => v !== "");

    servicioSelect.innerHTML =
      '<option value="">-- Elige un servicio --</option>';

    if (data.servicios && data.servicios.length > 0) {
      data.servicios.forEach((servicio) => {
        const option = document.createElement("option");
        option.value = servicio.id;
        option.textContent = `${servicio.nombre} - $${servicio.costo}`;
        option.dataset.costo = servicio.costo;

        // Deshabilitar si ya está seleccionado en otro select
        if (serviciosYaSeleccionados.includes(String(servicio.id))) {
          option.disabled = true;
          option.textContent += " (ya seleccionado)";
        }

        servicioSelect.appendChild(option);
      });
      servicioSelect.disabled = false;
    } else {
      servicioSelect.innerHTML =
        '<option value="">-- No hay servicios disponibles --</option>';
    }
  } catch (error) {
    console.error("Error:", error);
    mostrarToastExito("Error al cargar servicios", "error");
  }
}

// Cargar equipamiento por tipo
async function cargarEquipamientoPorTipo(tipoSelect, equipamentoSelect) {
  const tipoId = tipoSelect.value;

  if (!tipoId) {
    equipamentoSelect.innerHTML =
      '<option value="">-- Selecciona un tipo primero --</option>';
    equipamentoSelect.disabled = true;
    return;
  }

  try {
    const response = await fetch(
      `/reservacion/equipamiento-por-tipo/?tipo_id=${tipoId}`,
    );
    const data = await response.json();

    // Obtener equipamentos ya seleccionados en otros selects
    const equiposYaSeleccionados = Array.from(
      document.querySelectorAll(".equipamiento-select"),
    )
      .filter((s) => s !== equipamentoSelect)
      .map((s) => s.value)
      .filter((v) => v !== "");

    equipamentoSelect.innerHTML =
      '<option value="">-- Elige un equipamento --</option>';

    if (data.equipamientos && data.equipamientos.length > 0) {
      data.equipamientos.forEach((equip) => {
        const option = document.createElement("option");
        option.value = equip.id;
        option.textContent = `${equip.nombre} - $${equip.costo} (Stock: ${equip.stock})`;
        option.dataset.costo = equip.costo;
        option.dataset.stock = equip.stock;

        // Deshabilitar si ya está seleccionado en otro select
        if (equiposYaSeleccionados.includes(String(equip.id))) {
          option.disabled = true;
          option.textContent += " (ya seleccionado)";
        }

        equipamentoSelect.appendChild(option);
      });
      equipamentoSelect.disabled = false;
    } else {
      equipamentoSelect.innerHTML =
        '<option value="">-- No hay equipamentos disponibles --</option>';
    }
  } catch (error) {
    console.error("Error:", error);
    mostrarToastExito("Error al carregar equipamentos", "error");
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
    mobiliarioSelect.innerHTML =
      '<option value="">-- Selecciona un tipo primero --</option>';
    mobiliarioSelect.disabled = true;
    return;
  }

  try {
    const respuesta = await fetch(
      `/reservacion/mobiliarios-tipo/?tipo_id=${tipoId}`,
    );
    const data = await respuesta.json();

    const mobilariosSeleccionados = Array.from(
      document.querySelectorAll(".mobiliario-select"),
    )
      .filter((s) => s !== mobiliarioSelect)
      .map((s) => s.value)
      .filter((v) => v !== "");

    mobiliarioSelect.innerHTML =
      '<option value="">-- Elige un mobiliario --</option>';

    if (data.mobiliarios && data.mobiliarios.length > 0) {
      data.mobiliarios.forEach((mobiliario) => {
        const option = document.createElement("option");
        option.value = mobiliario.id;
        option.textContent = `${mobiliario.nombre} - $${mobiliario.costo} - Stock:${mobiliario.stock}`;
        option.dataset.costo = mobiliario.costo;

        if (mobilariosSeleccionados.includes(String(mobiliario.id))) {
          option.disabled = true;
          option.textContent += " (ya seleccionado)";
        }

        mobiliarioSelect.appendChild(option);
      });

      mobiliarioSelect.disabled = false;
    } else {
      mobiliarioSelect.innerHTML =
        '<option value="">-- No hay mobiliarios disponibles --</option>';
    }
  } catch (error) {
    console.error("Error:", error);
    mostrarToastExito("Error al cargar mobiliarios", "error");
  }
}

// Función para deshabilitar opciones seleccionadas
function actualizarOpcionesSelect(claseSelect) {
  const selects = document.querySelectorAll("." + claseSelect);

  if (selects.length === 0) return;

  // Obtener todos los valores seleccionados actualmente
  const valoresSeleccionados = Array.from(selects)
    .map((seleccion) => seleccion.value)
    .filter((valor) => valor !== "");

  // Recorrer cada select y deshabilitar/habilitar opciones
  selects.forEach(function (select) {
    Array.from(select.options).forEach(function (option) {
      // Si el valor ya está seleccionado en otro select, deshabilitar
      if (
        valoresSeleccionados.includes(option.value) &&
        option.value !== select.value
      ) {
        option.disabled = true;
      } else {
        option.disabled = false;
      }
    });
  });
}

// Event listeners
document.addEventListener("DOMContentLoaded", function () {
  // Servicios - listeners para todos los selects de tipo
  document.querySelectorAll(".servicio-tipo").forEach(function (select) {
    select.addEventListener("change", function () {
      const pair = this.closest(".servicio-pair");
      const servicioSelect = pair.querySelector(".servicio-select");
      cargarServiciosPorTipo(this, servicioSelect);
    });
  });

  // Servicios - listeners para deshabilitar opciones repetidas
  document.querySelectorAll(".servicio-select").forEach(function (select) {
    select.addEventListener("change", function () {
      actualizarOpcionesSelect("servicio-select");
    });
  });

  // Equipamientos - listeners para todos los selects de tipo
  document.querySelectorAll(".equipamiento-tipo").forEach(function (select) {
    select.addEventListener("change", function () {
      const pair = this.closest(".equipo-pair");
      const equipamentoSelect = pair.querySelector(".equipamiento-select");
      cargarEquipamientoPorTipo(this, equipamentoSelect);
    });
  });

  // Equipamientos - listeners para deshabilitar opciones repetidas
  document.querySelectorAll(".equipamiento-select").forEach(function (select) {
    select.addEventListener("change", function () {
      actualizarOpcionesSelect("equipamiento-select");
    });
  });

  const salonSeleccionado = document.getElementById("select-salon");
  if (salonSeleccionado) {
    salonSeleccionado.addEventListener("change", function () {
      cargarMontajesSalon(this.value);
    });
  }

  document.querySelectorAll(".mobiliario-tipo").forEach(function (select) {
    select.addEventListener("change", function () {
      const pair = this.closest(".mobil-pair");
      const mobiliarioSelect = pair.querySelector(".mobiliario-select");
      cargarMobiliariosPorTipo(this, mobiliarioSelect);
    });
  });

  document.querySelectorAll(".mobiliario-tipo").forEach(function (select) {
    select.addEventListener("change", function () {
      actualizarOpcionesSelect("mobiliario-select");
    });
  });
});
