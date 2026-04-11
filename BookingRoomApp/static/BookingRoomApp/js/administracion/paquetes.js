document.addEventListener("DOMContentLoaded", function () {
  // === PAQUETES ===
  let paqueteServicioIndex = 1;
  let paqueteEquipamientoIndex = 1;
  let paqueteMobiliarioIndex = 1;

  // pa calcular y poner el subtotal automaticamente en el campo subtotal
  window.calcularTotalAutomatico = function () {
    let subtotal = 0;

    // sumamos salon
    const salonSeleccionado = document.getElementById("paquete-salon-select");
    if (salonSeleccionado && salonSeleccionado.selectedIndex > 0) {
      subtotal +=
        parseFloat(
          salonSeleccionado.options[salonSeleccionado.selectedIndex].dataset
            .costo,
        ) || 0;
    }

    // sumamos servicios
    document
      .querySelectorAll(".paquete-servicio-select")
      .forEach((seleccionado) => {
        if (seleccionado.selectedIndex > 0 && !seleccionado.disabled) {
          subtotal +=
            parseFloat(
              seleccionado.options[seleccionado.selectedIndex].dataset.costo,
            ) || 0;
        }
      });

    // sumamos equipamientos
    document.querySelectorAll(".paquetes-equipamiento-pair").forEach((par) => {
      const seleccionado = par.querySelector(".paquete-equipamiento-select");
      const entradaCantidad = par.querySelector('input[type="number"]');

      if (
        seleccionado &&
        seleccionado.selectedIndex > 0 &&
        !seleccionado.disabled
      ) {
        const costo =
          parseFloat(
            seleccionado.options[seleccionado.selectedIndex].dataset.costo,
          ) || 0;
        const cantidad = parseInt(entradaCantidad.value) || 1;

        subtotal += costo * cantidad;
      }
    });

    // sumamos mobiliarios
    document.querySelectorAll(".paquetes-mobiliario-pair").forEach((par) => {
      const seleccionado = par.querySelector(".paquete-mobiliario-select");
      const entradaCantidad = par.querySelector('input[type="number"]');

      if (
        seleccionado &&
        seleccionado.selectedIndex > 0 &&
        !seleccionado.disabled
      ) {
        const costo =
          parseFloat(
            seleccionado.options[seleccionado.selectedIndex].dataset.costo,
          ) || 0;
        const cantidad = parseInt(entradaCantidad.value) || 1;

        subtotal += costo * cantidad;
      }
    });

    // lo ponemos visualmente en el input de subtotal
    const subtotalInput = document.getElementById("paquete-subtotal");
    if (subtotalInput) {
      subtotalInput.value = subtotal.toFixed(2);
      calcularPaqueteTotal();
    }
  };

  window.anadirPaqueteServicio = function () {
    paqueteServicioIndex++;
    const container = document.getElementById("paquete-servicios-list");
    const primerSelectTipo = document.querySelector(
      "#paquete-servicios-list .paquete-servicio-tipo",
    );
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";

    const html = `
      <div class="administrador-inputGrid paquetes-servicio-pair" data-index="${paqueteServicioIndex}">
        <label class="administrador-label">Tipo de servicio:<br>
          <select class="administrador-select paquete-servicio-tipo" name="servicio_tipo_${paqueteServicioIndex}">
            ${opcionesTipo}
          </select>
        </label>
        <label class="administrador-label">Seleccionar Servicio:<br>
          <select class="administrador-select paquete-servicio-select" name="servicio_${paqueteServicioIndex}" disabled>
            <option value="">-- Selecciona un tipo primero --</option>
          </select>
        </label>
      </div>
    `;
    container.insertAdjacentHTML("beforeend", html);
    agregarEventosPaqueteServicios();
  };

  window.anadirPaqueteEquipamiento = function () {
    paqueteEquipamientoIndex++;
    const container = document.getElementById("paquete-equipamientos-list");
    const primerSelectTipo = document.querySelector(
      "#paquete-equipamientos-list .paquete-equipamiento-tipo",
    );
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";

    const html = `
      <div class="administrador-inputGrid paquetes-equipamiento-pair" data-index="${paqueteEquipamientoIndex}">
        <label class="administrador-label">Tipo de equipamiento:<br>
          <select class="administrador-select paquete-equipamiento-tipo" name="equipamiento_tipo_${paqueteEquipamientoIndex}">
            ${opcionesTipo}
          </select>
        </label>
        <label class="administrador-label">Seleccionar Equipo:<br>
          <select class="administrador-select paquete-equipamiento-select" name="equipamiento_${paqueteEquipamientoIndex}" disabled>
            <option value="">-- Selecciona un tipo primero --</option>
          </select>
        </label>
        <label class="administrador-label">Cantidad:<br>
          <input type="number" class="administrador-input" name="equipamiento_cantidad_${paqueteEquipamientoIndex}" value="1" min="1">
        </label>
      </div>
    `;
    container.insertAdjacentHTML("beforeend", html);
    agregarEventosPaqueteEquipamientos();
  };

  window.anadirPaqueteMobiliarios = function () {
    paqueteMobiliarioIndex++;
    const container = document.getElementById("paquete-mobiliario-list");
    const primerSelectTipo = document.querySelector(
      "#paquete-mobiliario-list .paquete-mobiliario-tipo",
    );
    const opcionesTipo = primerSelectTipo ? primerSelectTipo.innerHTML : "";

    const html = `
      <div class="administrador-inputGrid paquetes-mobiliario-pair" data-index="${paqueteMobiliarioIndex}">
        <label class="administrador-label">Tipo de mobiliario:<br>
          <select class="administrador-select paquete-mobiliario-tipo" name="mobiliario_tipo_${paqueteMobiliarioIndex}">
            ${opcionesTipo}
          </select>
        </label>
        <label class="administrador-label">Seleccionar mobiliario:<br>
          <select class="administrador-select paquete-mobiliario-select" name="mobiliario_${paqueteMobiliarioIndex}" disabled>
            <option value="">-- Selecciona un tipo primero --</option>
          </select>
        </label>
        <label class="administrador-label">Cantidad:<br>
          <input type="number" class="administrador-input" name="mobiliario_cantidad_${paqueteMobiliarioIndex}" value="1" min="1">
        </label>
      </div>
    `;
    container.insertAdjacentHTML("beforeend", html);
    agregarEventosPaqueteMobiliarios();
  };

  window.quitarPaqueteItem = function (tipo) {
    var tipoDefinitivo;
    if (tipo === "servicios") {
      tipoDefinitivo = "paquete-servicios-list";
    } else if (tipo === "equipamientos") {
      tipoDefinitivo = "paquete-equipamientos-list";
    } else if (tipo === "mobiliario") {
      tipoDefinitivo = "paquete-mobiliario-list";
    }

    const container = document.getElementById(tipoDefinitivo);
    if (container && container.children.length > 1) {
      container.removeChild(container.lastElementChild);
    }
  };

  async function cargarPaqueteServiciosPorTipo(tipoSelect, servicioSelect) {
    const tipoId = tipoSelect.value;
    if (!tipoId) {
      servicioSelect.innerHTML =
        '<option value="">-- Selecciona un tipo primero --</option>';
      servicioSelect.disabled = true;
      return null;
    }

    try {
      const response = await fetch(
        `/reservacion/servicios-por-tipo/?tipo_id=${tipoId}`,
      );
      const data = await response.json();

      const serviciosYaSeleccionados = Array.from(
        document.querySelectorAll(".paquete-servicio-select"),
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
    }
  }

  async function cargarPaqueteEquipamientoPorTipo(
    tipoSelect,
    equipamentoSelect,
  ) {
    const tipoId = tipoSelect.value;
    if (!tipoId) {
      equipamentoSelect.innerHTML =
        '<option value="">-- Selecciona un tipo primero --</option>';
      equipamentoSelect.disabled = true;
      return null;
    }

    try {
      const response = await fetch(
        `/reservacion/equipamiento-por-tipo/?tipo_id=${tipoId}`,
      );
      const data = await response.json();

      const equiposYaSeleccionados = Array.from(
        document.querySelectorAll(".paquete-equipamiento-select"),
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
          option.textContent = `${equip.nombre} - $${equip.costo} (Stock: ${equip.stockTotal})`;
          option.dataset.costo = equip.costo;
          option.dataset.stock = equip.stockTotal;

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
    }
  }

  async function cargarPaqueteMobiliarioPorTipo(tipoSelect, mobiliarioSelect) {
    const tipoId = tipoSelect.value;
    if (!tipoId) {
      mobiliarioSelect.innerHTML =
        '<option value="">-- Selecciona un tipo primero --</option>';
      mobiliarioSelect.disabled = true;
      return null;
    }

    try {
      const response = await fetch(
        `/reservacion/mobiliarios-tipo/?tipo_id=${tipoId}`,
      );
      const data = await response.json();

      const mobiliarioYaSeleccionados = Array.from(
        document.querySelectorAll(".paquete-mobiliario-select"),
      )
        .filter((s) => s !== mobiliarioSelect)
        .map((s) => s.value)
        .filter((v) => v !== "");

      mobiliarioSelect.innerHTML =
        '<option value="">-- Elige un Mobiliario --</option>';

      if (data.mobiliarios && data.mobiliarios.length > 0) {
        data.mobiliarios.forEach((mob) => {
          const option = document.createElement("option");
          option.value = mob.id;
          option.textContent = `${mob.nombre} - $${mob.costo} (Stock: ${mob.stockTotal})`;
          option.dataset.costo = mob.costo;
          option.dataset.stock = mob.stockTotal;

          if (mobiliarioYaSeleccionados.includes(String(mob.id))) {
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
    }
  }

  window.actualizarOpcionesPaquete = function (claseSelect) {
    const selects = document.querySelectorAll("." + claseSelect);
    if (selects.length === 0) return null;

    const valoresSeleccionados = Array.from(selects)
      .map((s) => s.value)
      .filter((v) => v !== "");
    selects.forEach(function (select) {
      Array.from(select.options).forEach(function (option) {
        if (
          valoresSeleccionados.includes(option.value) &&
          option.value !== select.value
        ) {
          option.disabled = true;
        } else if (!option.disabled) {
          option.disabled = false;
        }
      });
    });
  };

  function agregarEventosPaqueteServicios() {
    document
      .querySelectorAll(".paquete-servicio-tipo")
      .forEach(function (select) {
        select.addEventListener("change", function () {
          const pair = this.closest(".paquetes-servicio-pair");
          const servicioSelect = pair.querySelector(".paquete-servicio-select");
          cargarPaqueteServiciosPorTipo(this, servicioSelect);
        });
      });

    document
      .querySelectorAll(".paquete-servicio-select")
      .forEach(function (select) {
        select.addEventListener("change", function () {
          actualizarOpcionesPaquete("paquete-servicio-select");
          calcularTotalAutomatico();
        });
      });
  }

  function agregarEventosPaqueteEquipamientos() {
    document
      .querySelectorAll(".paquete-equipamiento-tipo")
      .forEach(function (select) {
        select.addEventListener("change", function () {
          const pair = this.closest(".paquetes-equipamiento-pair");
          const equipamentoSelect = pair.querySelector(
            ".paquete-equipamiento-select",
          );
          cargarPaqueteEquipamientoPorTipo(this, equipamentoSelect);
        });
      });

    document
      .querySelectorAll(".paquete-equipamiento-select")
      .forEach(function (select) {
        select.addEventListener("change", function () {
          actualizarOpcionesPaquete("paquete-equipamiento-select");

          const par = this.closest(".paquetes-equipamiento-pair");
          const intpuCantidad = par.querySelector('input[type="number"]');
          const opcionSeleccionada = this.options[this.selectedIndex];

          if (opcionSeleccionada && opcionSeleccionada.dataset.stock) {
            const stockmaximo = parseInt(opcionSeleccionada.dataset.stock);
            intpuCantidad.max = stockmaximo;

            if (parseInt(intpuCantidad.value) > stockmaximo) {
              intpuCantidad.value = stockmaximo;
              alert(
                `Se ajusto la cantidad. Solo hay ${stockmaximo} disponibles del equipamiento seleccionado`,
              );
            }
          }

          calcularTotalAutomatico();
        });
      });

    document
      .querySelectorAll('input[name^="equipamiento_cantidad_"]')
      .forEach((input) => {
        input.addEventListener("input", function () {
          if (this.max && parseInt(this.value) > parseInt(this.max)) {
            this.value = this.max;
          }
          calcularTotalAutomatico();
        });
      });
  }

  function agregarEventosPaqueteMobiliarios() {
    document
      .querySelectorAll(".paquete-mobiliario-tipo")
      .forEach(function (select) {
        select.addEventListener("change", function () {
          const pair = this.closest(".paquetes-mobiliario-pair");
          const mobiliarioSelect = pair.querySelector(
            ".paquete-mobiliario-select",
          );
          cargarPaqueteMobiliarioPorTipo(this, mobiliarioSelect);
        });
      });

    document
      .querySelectorAll(".paquete-mobiliario-select")
      .forEach(function (select) {
        select.addEventListener("change", function () {
          actualizarOpcionesPaquete("paquete-mobiliario-select");
          const par = this.closest(".paquetes-mobiliario-pair");
          const inputCantidad = par.querySelector('input[type="number"]');
          const opcionSeleccionada = this.options[this.selectedIndex];
          if (opcionSeleccionada && opcionSeleccionada.dataset.stock) {
            const stockMaximo = parseInt(opcionSeleccionada.dataset.stock);
            inputCantidad.max = stockMaximo;
            if (parseInt(inputCantidad.value) > stockMaximo) {
              inputCantidad.value = stockMaximo;
              alert(
                `Se ajusto la cantidad. Solo hay ${stockMaximo} disponibles del mobiliario seleccionado.`,
              );
            }
          }
          calcularTotalAutomatico();
        });
      });

    document
      .querySelectorAll('input[name^="mobiliario_cantidad_"]')
      .forEach((input) => {
        input.addEventListener("input", function () {
          if (this.max && parseInt(this.value) > parseInt(this.max)) {
            this.value = this.max;
          }
          calcularTotalAutomatico();
        });
      });
  }

  // Calcular total
  window.calcularPaqueteTotal = function () {
    const subtotal =
      parseFloat(document.getElementById("paquete-subtotal").value) || 0;
    const iva = parseFloat(document.getElementById("paquete-iva").value) || 0;
    const total = subtotal + (subtotal * iva) / 100;
    const totalInput = document.getElementById("paquete-total");
    if (totalInput) totalInput.value = total.toFixed(2);
  };

  // armar el json pa envialo a registrar
  window.armarJson = function () {
    const salon = document.getElementById("paquete-salon-select");
    if (!salon || !salon.value) {
      alert("Por favor seleccionar un salon");
      return null;
    }

    const montaje = document.getElementById("paquete-montaje-select");
    if (!montaje || !montaje.value) {
      alert("Por favor seleccionar un tipo de montaje");
      return null;
    }

    const nombre = document.getElementById("paquete-nombre");
    if (!nombre || !nombre.value) {
      alert("Por favor ingresa un nombre para el paquete");
      return null;
    }

    const descripEvento = document.getElementById("paquete-descripEvento");
    if (!descripEvento || !descripEvento.value) {
      alert("Por favor ingrese una descripEvento para el paquete");
      return null;
    }

    const tipo_evento = document.getElementById("paquete-tipo-evento");
    if (!tipo_evento || !tipo_evento.value) {
      alert("Por favor seleccionar un tipo de evento");
      return null;
    }

    const asistentes = document.getElementById("paquete-asistentes");
    const opcionSalon = salon.options[salon.selectedIndex];
    const capacidadSalon = parseInt(opcionSalon.dataset.capacidad) || 0;
    const numAsistentes = parseInt(asistentes.value) || 0;

    if (capacidadSalon < numAsistentes) {
      alert(
        `El salón no soporta tantas personas. Capacidad máxima: ${capacidadSalon}`,
      );
      return null;
    }

    const mobiliarios = [];
    document.querySelectorAll(".paquetes-mobiliario-pair").forEach((par) => {
      const mob = par.querySelector(".paquete-mobiliario-select");
      const cantidad = par.querySelector('input[type="number"]');
      if (mob && cantidad && mob.value && cantidad.value) {
        mobiliarios.push({
          id: parseInt(mob.value),
          cantidad: parseInt(cantidad.value),
        });
      }
    });
    if (mobiliarios.length === 0) {
      alert("Por favor seleccionar mobiliarios");
      return null;
    }

    const reserva_servicio = [];
    document.querySelectorAll(".paquetes-servicio-pair").forEach((par) => {
      const servicio = par.querySelector(".paquete-servicio-select");
      if (servicio && servicio.value) {
        reserva_servicio.push({
          id: parseInt(servicio.value),
        });
      }
    });

    const reserva_equipa = [];
    document.querySelectorAll(".paquetes-equipamiento-pair").forEach((par) => {
      const equipo = par.querySelector(".paquete-equipamiento-select");
      const cantidad = par.querySelector('input[type="number"]');
      if (equipo && equipo.value && cantidad && cantidad.value) {
        reserva_equipa.push({
          id: parseInt(equipo.value),
          cantidad: parseInt(cantidad.value),
        });
      }
    });

    const subtotal = document.getElementById("paquete-subtotal");
    if (!subtotal || !subtotal.value || parseFloat(subtotal.value) <= 0.0) {
      alert("Porfavor introducir un valor al subtotal de venta");
      return null;
    }

    return {
      nombre: nombre.value.trim(),
      descripEvento: descripEvento.value.trim(),
      estimaAsistentes: parseInt(asistentes.value),
      estado_reserva: "PAQUE",
      reserva_servicio: reserva_servicio,
      reserva_equipa: reserva_equipa,
      montaje: {
        salon: parseInt(salon.value),
        tipo_montaje: parseInt(montaje.value),
        mobiliarios: mobiliarios,
      },
      tipo_evento: tipo_evento.value,
      subtotal: parseFloat(subtotal.value),
    };
  };

  // Guardar paquete
  window.guardarPaquete = async function () {
    const paquete = armarJson();

    if (!paquete) return null;

    try {
      const respuesta = await fetch("/api/reservacion/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(paquete),
      });
      if (respuesta.ok || respuesta.status === 201) {
        const data = await respuesta.json();
        alert("Paquete creado con exito");
        window.location.reload();
      } else {
        const error = await respuesta.json();
        console.error("Django no jalo checa eso", error);
        alert("Error al guardar el paquete. Revisar consola.");
      }
    } catch (e) {
      console.error("Error critico:", e);
      alert("No se pudo conectar al servidor");
    }
  };

  window.eliminarPaquete = async function (id) {
    if (
      !confirm(
        "Seguro de eliminar este paquete? Esta accion no se puede revertir",
      )
    ) {
      return;
    }

    try {
      const respeusta = await fetch(`/api/reservacion/${id}/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
      });

      if (respeusta.ok | (respeusta.status === 204)) {
        alert("Paquete eliminado correctamente");
        window.location.reload();
      } else {
        const error = await respeusta.json();
        console.error("Error al eliminar: ", error);
        alert("Surgio un probblema al eliminar el paquete.");
      }
    } catch (error) {
      console.error("Error en la conexion con la red: ", error);
      alert("No se pudo conectar al servidor para la eliminacion del paquete.");
    }
  };

  agregarEventosPaqueteServicios();
  agregarEventosPaqueteEquipamientos();
  agregarEventosPaqueteMobiliarios();

  const salonSeleccionado = document.getElementById("paquete-salon-select");
  if (salonSeleccionado)
    salonSeleccionado.addEventListener("change", calcularTotalAutomatico);
  const subtotalInput = document.getElementById("paquete-subtotal");
  const ivaInput = document.getElementById("paquete-iva");
  if (subtotalInput)
    subtotalInput.addEventListener("input", calcularPaqueteTotal);
  if (ivaInput) ivaInput.addEventListener("input", calcularPaqueteTotal);
});

const catalogosEdit = { servicios: [], mobiliarios: [], equipamientos: [] };

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const [resS, resM, resE] = await Promise.all([
      fetch("/api/servicio/"),
      fetch("/api/mobiliario/"),
      fetch("/api/equipamiento/"),
    ]);
    if (resS.ok) catalogosEdit.servicios = await resS.json();
    if (resM.ok) catalogosEdit.mobiliarios = await resM.json();
    if (resE.ok) catalogosEdit.equipamientos = await resE.json();
  } catch (e) {
    console.error("Error precargando catálogos para edición", e);
  }
});

window.agregarFilaEdicion = function (tipoEntidad, valorId = "", cantidad = 1) {
  const container = document.getElementById(`edit-${tipoEntidad}-list`);
  const catalogoItems =
    tipoEntidad === "mobiliario"
      ? catalogosEdit.mobiliarios
      : tipoEntidad === "servicio"
        ? catalogosEdit.servicios
        : catalogosEdit.equipamientos;

  const claseOriginal =
    tipoEntidad === "mobiliario"
      ? ".paquete-mobiliario-tipo"
      : tipoEntidad === "servicio"
        ? ".paquete-servicio-tipo"
        : ".paquete-equipamiento-tipo";
  const selectOriginal = document.querySelector(claseOriginal);
  const opcionesTipoHtml = selectOriginal
    ? selectOriginal.innerHTML
    : '<option value="">-- Tipo --</option>';

  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = `<select>${opcionesTipoHtml}</select>`;
  const mapaTipos = {};
  const mapaTiposInverso = {};
  tempDiv.querySelectorAll("option").forEach((opt) => {
    if (opt.value) {
      mapaTipos[String(opt.value).trim()] = opt.textContent.trim();
      mapaTiposInverso[opt.textContent.trim().toLowerCase()] = String(
        opt.value,
      ).trim();
    }
  });

  const obtenerIdTipo = (item) => {
    let rawValue = null;
    if (item.tipo_movil) rawValue = item.tipo_movil;
    else if (item.tipo_servicio) rawValue = item.tipo_servicio;
    else if (item.tipo_equipa) rawValue = item.tipo_equipa;
    else {
      for (let key in item) {
        if (key.toLowerCase().includes("tipo") && item[key]) {
          rawValue = item[key];
          break;
        }
      }
    }

    if (!rawValue) return null;
    if (typeof rawValue === "object" && rawValue.id) return String(rawValue.id);

    const strVal = String(rawValue).trim().toLowerCase();
    if (mapaTipos[strVal]) return strVal;
    if (mapaTiposInverso[strVal]) return mapaTiposInverso[strVal];

    return String(rawValue);
  };

  let tipoPreseleccionado = "";
  if (valorId) {
    const itemEncontrado = catalogoItems.find(
      (i) => String(i.id) === String(valorId),
    );
    if (itemEncontrado) tipoPreseleccionado = obtenerIdTipo(itemEncontrado);
  }

  const divFila = document.createElement("div");
  divFila.className = `edit-fila-${tipoEntidad}`;
  divFila.style =
    "display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px; background: #fff; padding: 12px; border-radius: 8px; border: 1px solid #caced1; box-shadow: 0 2px 4px rgba(0,0,0,0.05);";

  let html = `<select class="administrador-select edit-tipo-selector" style="width: 100%; padding: 8px;">
                    ${opcionesTipoHtml}
                </select>`;

  html += `<select class="administrador-select edit-item-${tipoEntidad}" style="width: 100%; padding: 8px;" ${!tipoPreseleccionado ? "disabled" : ""}>
                <option value="">-- Selecciona --</option>`;
  if (tipoPreseleccionado) {
    catalogoItems
      .filter((i) => String(obtenerIdTipo(i)) === String(tipoPreseleccionado))
      .forEach((item) => {
        html += `<option value="${item.id}" ${String(item.id) === String(valorId) ? "selected" : ""}>${item.nombre}</option>`;
      });
  }
  html += `</select>`;

  html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-top: 5px;">`;
  if (tipoEntidad !== "servicio") {
    html += `<div style="display:flex; align-items:center; gap:5px;">
                    <label style="font-size: 12px; color: #555; font-weight: bold;">Cant:</label>
                    <input type="number" class="administrador-input edit-cantidad-${tipoEntidad}" value="${cantidad}" min="1" style="width: 70px; padding: 5px; margin: 0;">
                 </div>`;
  } else {
    html += `<div></div>`;
  }
  html += `<button type="button" onclick="this.closest('.edit-fila-${tipoEntidad}').remove()" style="background: #ff4d4d; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; font-weight: bold;">Eliminar</button>`;
  html += `</div>`;

  divFila.innerHTML = html;
  container.appendChild(divFila);

  const tipoSelect = divFila.querySelector(".edit-tipo-selector");
  const itemSelect = divFila.querySelector(`.edit-item-${tipoEntidad}`);

  if (tipoPreseleccionado) {
    tipoSelect.value = tipoPreseleccionado;
  }

  tipoSelect.addEventListener("change", () => {
    const tId = tipoSelect.value.trim();
    let opcionesHtml = '<option value="">-- Selecciona --</option>';

    if (tId) {
      const filtrados = catalogoItems.filter(
        (i) => String(obtenerIdTipo(i)) === tId,
      );
      filtrados.forEach((item) => {
        opcionesHtml += `<option value="${item.id}">${item.nombre}</option>`;
      });
      itemSelect.innerHTML = opcionesHtml;
      itemSelect.disabled = false;
    } else {
      itemSelect.innerHTML = opcionesHtml;
      itemSelect.disabled = true;
    }
  });
};

window.editarPaquete = async function (id) {
  try {
    const response = await fetch(`/api/reservacion/${id}/`);
    if (!response.ok) throw new Error("Error fetching");
    const data = await response.json();

    document.getElementById("edit-paquete-id").value = data.id;
    document.getElementById("edit-nombre").value = data.nombreEvento;
    document.getElementById("edit-asistentes").value = data.estimaAsistentes;
    document.getElementById("edit-subtotal").value = data.subtotal;
    document.getElementById("edit-salon").value = data.montaje?.salon?.nombre || "-";
    document.getElementById("edit-montaje").value = data.montaje?.tipo_montaje?.nombre || "-";
    document.getElementById("edit-descripEvento").value = data.descripEvento || "";

    ["mobiliario", "servicio", "equipamiento"].forEach(
      (t) => (document.getElementById(`edit-${t}-list`).innerHTML = ""),
    );

    if (data.montaje?.montaje_mobiliario) {
      data.montaje.montaje_mobiliario.forEach((m) => {
        const idMob = m.mobiliario?.id || m.mobiliario;
        agregarFilaEdicion("mobiliario", idMob, m.cantidad);
      });
    }
    if (data.reserva_servicio) {
      data.reserva_servicio.forEach((s) => {
        const idServ = s.servicio?.id || s.servicio;
        agregarFilaEdicion("servicio", idServ);
      });
    }
    if (data.reserva_equipa) {
      data.reserva_equipa.forEach((e) => {
        const idEq = e.equipamiento?.id || e.equipamiento;
        agregarFilaEdicion("equipamiento", idEq, e.cantidad);
      });
    }

    document.getElementById("modal-editar-paquete").showModal();
  } catch (e) {
    console.error(e);
    alert("No se pudo cargar el paquete. Revisa que el ID sea correcto.");
  }
};

window.guardarEdicionPaquete = async function () {
  const id = document.getElementById("edit-paquete-id").value;
  const subtotal = parseFloat(document.getElementById("edit-subtotal").value) || 0;

  const payload = {
    nombreEvento: document.getElementById("edit-nombre").value.trim(),
    descripEvento: document.getElementById("edit-descripEvento").value.trim(),
    estimaAsistentes: parseInt(document.getElementById("edit-asistentes").value) || 0,
    subtotal: subtotal,
    mobiliarios: [],
    reserva_servicio: [],
    reserva_equipa: [],
  };

  document.querySelectorAll(".edit-fila-mobiliario").forEach((fila) => {
    const nodoItem = fila.querySelector(".edit-item-mobiliario");
    const nodoCant = fila.querySelector(".edit-cantidad-mobiliario");
    if (nodoItem && nodoCant && nodoItem.value) {
      payload.mobiliarios.push({ 
          id: parseInt(nodoItem.value), 
          cantidad: parseInt(nodoCant.value) || 1 
      });
    }
  });

  document.querySelectorAll(".edit-fila-servicio").forEach((fila) => {
    const nodoItem = fila.querySelector(".edit-item-servicio");
    if (nodoItem && nodoItem.value) {
      payload.reserva_servicio.push({ 
          id: parseInt(nodoItem.value) 
      });
    }
  });

  document.querySelectorAll(".edit-fila-equipamiento").forEach((fila) => {
    const nodoItem = fila.querySelector(".edit-item-equipamiento");
    const nodoCant = fila.querySelector(".edit-cantidad-equipamiento");
    if (nodoItem && nodoCant && nodoItem.value) {
      payload.reserva_equipa.push({ 
          id: parseInt(nodoItem.value), 
          cantidad: parseInt(nodoCant.value) || 1 
      });
    }
  });

  try {
    const response = await fetch(`/api/reservacion/${id}/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      alert("Paquete actualizado correctamente.");
      window.location.reload();
    } else {
      const err = await response.json();
      console.error("Error del backend:", err);
      alert("Error al actualizar. Verifica que los datos estén completos.");
    }
  } catch (e) {
    console.error("Error de conexión:", e);
    alert("Falló la conexión con el servidor.");
  }
};
