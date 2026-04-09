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
      <div class="paquetes-mobiliario-pair" data-index="${paqueteMobiliarioIndex}">
        <div class="paquetes-campo">
          <label class="paquetes-label">Tipo de mobiliario</label>
          <select class="paquetes-input paquete-mobiliario-tipo" name="mobiliario_tipo_${paqueteMobiliarioIndex}">
            ${opcionesTipo}
          </select>
        </div>
        <div class="paquetes-campo">
          <label class="paquetes-label">Seleccionar mobiliario</label>
          <select class="paquetes-input paquete-mobiliario-select" name="mobiliario_${paqueteMobiliarioIndex}" disabled>
            <option value="">-- Selecciona un tipo primero --</option>
          </select>
        </div>
        <div class="paquetes-campo">
          <label class="paquetes-label">Cantidad</label>
          <input type="number" class="paquetes-input" name="mobilairio_cantidad_${paqueteMobiliarioIndex}" value="1" min="1">
        </div>
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

    const descripcion = document.getElementById("paquete-descripcion");
    if (!descripcion || !descripcion.value) {
      alert("Por favor ingrese una descripcion para el paquete");
      return null;
    }

    const tipo_evento = document.getElementById("paquete-tipo-evento");
    if (!tipo_evento || !tipo_evento.value) {
      alert("Por favor seleccionar un tipo de evento");
      return null;
    }

    const asistentes = document.getElementById("paquete-asistentes");
    if (salon.dataset.capacidad <= asistentes) {
      alert("El salon no soporta tantas personas");
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
      descripEvento: descripcion.value.trim(),
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

  // Inicializar eventos
  agregarEventosPaqueteServicios();
  agregarEventosPaqueteEquipamientos();
  agregarEventosPaqueteMobiliarios();

  // Eventos para cálculo de total
  const salonSeleccionado = document.getElementById("paquete-salon-select");
  if (salonSeleccionado)
    salonSeleccionado.addEventListener("change", calcularTotalAutomatico);
  const subtotalInput = document.getElementById("paquete-subtotal");
  const ivaInput = document.getElementById("paquete-iva");
  if (subtotalInput)
    subtotalInput.addEventListener("input", calcularPaqueteTotal);
  if (ivaInput) ivaInput.addEventListener("input", calcularPaqueteTotal);
});
