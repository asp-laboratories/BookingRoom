let opcionesServicio = "";
let opcionesEquipo = "";
let opcionesMobiliario = "";

let opcionesTipoServicio = "";
let opcionesTipoEquipo = "";
let opcionesTipoMobiliario = "";

async function cargarCatalogos() {
  try {
    const resTiposMob = await fetch('/api/tipo-mobiliario/');
    const tiposMob = await resTiposMob.json();
    opcionesTipoMobiliario = tiposMob.map(t => `<option value="${t.id}">${t.nombre}</option>`).join('');

    const resMob = await fetch('/api/mobiliario/');
    const mobs = await resMob.json();
    opcionesMobiliario = mobs.map(m => `<option value="${m.id}" data-tipo="${m.tipo_movil.id}">${m.nombre}</option>`).join('');

    const resTiposEquipa = await fetch('/api/tipo-equipa/');
    const tiposEquipa = await resTiposEquipa.json();
    opcionesTipoEquipo = tiposEquipa.map(tipo => `<option value="${tipo.id}">${tipo.nombre}</option>`).join('');

    const resEquipos = await fetch('/api/equipamiento/');
    const equipos = await resEquipos.json();
    opcionesEquipo = equipos.map(equipo => `<option value="${equipo.id}" data-tipo="${equipo.tipo_equipa.id}">${equipo.nombre}</option>`).join('');

    const resTiposServicios = await fetch('/api/tipo-servicio/');
    const tiposServicios = await resTiposServicios.json();
    opcionesTipoServicio = tiposServicios.map(ts => `<option value="${ts.nombre}">${ts.nombre}</option>`).join('');

    const resServicios = await fetch('/api/servicio/');
    const servicios =  await resServicios.json();
    opcionesServicio = servicios.map(s => `<option value="${s.id}" data-tipo="${s.tipo_servicio}">${s.nombre}</option>`).join('');

  }
  catch (e) {
    console.error("Error al cargar los catalogos: ", e);
  }
}

function insertarFilaEdicion(tipo, cantidad = 1) {
  let contenedor,
    opcionesTipo,
    opcionesFinales,
    claseFila,
    extraHTML = "";

  if (tipo === "servicio") {
    contenedor = document.getElementById("edit-servicios-list");
    opcionesTipo = opcionesTipoServicio;
    opcionesFinales = opcionesServicio;
    claseFila = "fila-servicio";
  } else if (tipo === "equipo") {
    contenedor = document.getElementById("edit-equipos-list");
    opcionesTipo = opcionesTipoEquipo;
    opcionesFinales = opcionesEquipo;
    claseFila = "fila-equipo";
    extraHTML = `<input type="number" class="item-cantidad" value="${cantidad}" min="1" style="width: 65px; margin: 0; padding: 4px; font-size: 13px; height: 32px;">`;
  } else if (tipo === "mobiliario") {
    contenedor = document.getElementById("edit-mobiliarios-list");
    opcionesTipo = opcionesTipoMobiliario;
    opcionesFinales = opcionesMobiliario;
    claseFila = "fila-mobiliario";
    extraHTML = `<input type="number" class="item-cantidad" value="${cantidad}" min="1" style="width: 65px; margin: 0; padding: 4px; font-size: 13px; height: 32px;">`;
  }

  if (!contenedor) return;

  const idUnico = Date.now() + Math.floor(Math.random() * 1000);
  const idSelectTipo = `select-tipo-${idUnico}`;
  const idSelectFinal = `select-final-${idUnico}`;

  const html = `
    <div class="${claseFila}" style="display: flex; gap: 8px; align-items: center; margin-bottom: 8px;">
      
      <select id="${idSelectTipo}" class="tipo-select" style="flex: 1; margin: 0; padding: 4px 8px; font-size: 13px; height: 32px;" onchange="filtrarOpciones(this, '${idSelectFinal}', '${tipo}')">
        <option value="">-- Filtro --</option>
        ${opcionesTipo}
      </select>

      <select id="${idSelectFinal}" class="item-select" style="flex: 1; margin: 0; padding: 4px 8px; font-size: 13px; height: 32px;" disabled>
        <option value="">-- Seleccione --</option>
        ${opcionesFinales}
      </select>

      ${extraHTML}
      <button type="button" class="btn-modal btn-denegar" onclick="this.parentElement.remove()" style="padding: 0 10px; margin: 0; height: 32px; line-height: 1;">X</button>
    </div>
  `;
  contenedor.insertAdjacentHTML("beforeend", html);
  return idUnico;
}

function filtrarOpciones(tipoSeleccionado, idSeleccionado, tipoCategoria) {
  const selectFinal = document.getElementById(idSeleccionado);
  const valorTipo = tipoSeleccionado.value;

  if (!valorTipo) {
    selectFinal.disabled = true;
    selectFinal.value = "";
    Array.from(selectFinal.options).forEach((opt) => {
      if (opt.value !== "") opt.style.display = "none";
    });
    return;
  }

  selectFinal.disabled = false;
  selectFinal.value = ""; 

  Array.from(selectFinal.options).forEach((opt) => {
    if (opt.value === "") {
      opt.style.display = "block";
    } else {
      if (opt.getAttribute("data-tipo") === valorTipo) {
        opt.style.display = "block";
      } else {
        opt.style.display = "none";
      }
    }
  });
}

function anadirServicioEdit() {
  insertarFilaEdicion("servicio");
}

function anadirEquipoEdit() {
  insertarFilaEdicion("equipo");
}

function anadirMobiliarioEdit() {
  insertarFilaEdicion("mobiliario");
}

function abrirPagos() {
  document.getElementById("modalPagos").classList.add("mostrar");
}

function cerrarPagos() {
  document.getElementById("modalPagos").classList.remove("mostrar");
}

function abrirBEO() {
  document.getElementById("modalBEO").classList.add("mostrar");
}

function cerrarBEO() {
  document.getElementById("modalBEO").classList.remove("mostrar");
}

window.onclick = function (event) {
  let pagos = document.getElementById("modalPagos");
  let beo = document.getElementById("modalBEO");

  if (event.target == pagos) {
    pagos.classList.remove("mostrar");
  }

  if (event.target == beo) {
    beo.classList.remove("mostrar");
  }
};

document.addEventListener("DOMContentLoaded", async function () {

  await cargarCatalogos();

  document.querySelectorAll(".ver-pagos").forEach((btn) => {
    btn.addEventListener("click", function () {
      const pk = this.dataset.pk;
      fetch(`/recepcion/historial/${pk}/json/`)
        .then((response) => response.json())
        .then((data) => {
          document.getElementById("subtotal-modal").textContent =
            `Subtotal: $${data.subtotal}`;
          document.getElementById("iva-modal").textContent =
            `IVA: $${data.iva}`;
          document.getElementById("total-modal").textContent =
            `Total: $${data.total}`;
          document.getElementById("primer-pago").textContent =
            `Primer pago: $${data.primer_pago}`;
          document.getElementById("segundo-pago").textContent =
            `Segundo pago: $${data.segundo_pago}`;
          document.getElementById("saldo").textContent =
            `Saldo: $${data.saldo}`;
          document.getElementById("modalPagos").classList.add("mostrar");
        })
        .catch((error) => {
          console.error("Error:", error);
          mostrarToastExito("No se pudo cargar los pagos", "error");
        });
    });
  });

  document.querySelectorAll(".ver-beo").forEach((btn) => {
    btn.addEventListener("click", async function () {
      const pk = this.dataset.pk;

      try {
        const response = await fetch(`/home/${pk}/json/`);
        if (!response.ok) throw new Error("Error al obtener datos");

        const data = await response.json();

        document.getElementById("beo-titulo-evento").textContent =
          data.nombre_evento || "Orden de banquete de evento (BEO)";

        const spanTipo = document.getElementById("beo-tipo-documento");
        if (spanTipo) {
          if (data.estado === "SOLIC" || data.estado === "Solicitud") {
            spanTipo.textContent = "Solicitud Para: ";
          } else {
            spanTipo.textContent = "Reservacion Para: ";
          }
        }

        document.getElementById("beo-cliente-nombre").textContent =
          `${data.cliente.nombre} ${data.cliente.apellido_paterno} ${data.cliente.apellido_materno}`;
        document.getElementById("beo-cliente-correo").textContent =
          data.cliente.correo;
        document.getElementById("beo-cliente-telefono").textContent =
          data.cliente.telefono;
        document.getElementById("beo-cliente-rfc").textContent =
          data.cliente.rfc;
        document.getElementById("beo-cliente-nombre-fiscal").textContent =
          data.cliente.nombre_fiscal;

        document.getElementById("beo-evento-nombre").textContent =
          data.nombre_evento;
        document.getElementById("beo-evento-descripcion").textContent =
          data.descripcion;
        document.getElementById("beo-evento-fecha").textContent = data.fecha;
        document.getElementById("beo-evento-horario").textContent =
          `${data.hora_inicio} - ${data.hora_fin}`;
        document.getElementById("beo-evento-estado").textContent = data.estado;
        document.getElementById("beo-evento-asistentes").textContent =
          data.asistentes;

        document.getElementById("beo-salon-nombre").textContent = data.salon;
        document.getElementById("beo-salon-montaje").textContent = data.montaje;

        const serviciosSpan = document.getElementById("beo-servicios-lista");
        if (data.servicios && data.servicios.length > 0) {
          serviciosSpan.textContent = data.servicios.join(", ");
        } else {
          serviciosSpan.textContent = "No hay servicios";
        }

        const equipamientSpan = document.getElementById(
          "beo-equipamientos-lista",
        );
        if (data.equipamientos && data.equipamientos.length > 0) {
          equipamientSpan.textContent = data.equipamientos.join(", ");
        } else {
          equipamientSpan.textContent = "No hay equipamientos";
        }

        document.getElementById("beo-total-iva").textContent = `$${data.iva}`;
        document.getElementById("beo-total-subtotal").textContent =
          `$${data.subtotal}`;
        document.getElementById("beo-total-total").textContent =
          `$${data.total}`;

        const botones = document.getElementById("botones-modal");

        if (botones) {
          if (data.estado === "SOLIC" || data.estado === "Solicitud") {
            botones.style.display = "flex";
          } else {
            botones.style.display = "none";
          }
        }

        const modalElement = document.getElementById("modalBEO");
        if (modalElement) {
          modalElement.dataset.pk = pk;
          window.modalBEO.showModal();
        }
        
      } catch (error) {
        console.error("Error:", error);
        mostrarToastExito(
          "No se pudo cargar los detalles de la reservación",
          "error",
        );
      }
    });
  });

  let valoresOriginales = {};

  document.querySelectorAll(".editar-reservacion").forEach((btn) => {
    btn.addEventListener("click", async function () {
      const pk = this.dataset.pk;

      try {
        const response = await fetch(`/home/${pk}/json/`);
        if (!response.ok) throw new Error("Error al obtener datos");

        const data = await response.json();

        document.getElementById("edit-cliente-nombre").value =
          data.cliente.nombre || "";
        document.getElementById("edit-cliente-apellido-paterno").value =
          data.cliente.apellido_paterno || "";
        document.getElementById("edit-cliente-apellido-materno").value =
          data.cliente.apellido_materno || "";
        document.getElementById("edit-cliente-correo").value =
          data.cliente.correo || "";
        document.getElementById("edit-cliente-telefono").value =
          data.cliente.telefono || "";
        document.getElementById("edit-cliente-rfc").value =
          data.cliente.rfc || "";
        document.getElementById("edit-cliente-nombre-fiscal").value =
          data.cliente.nombre_fiscal || "";

        document.getElementById("edit-evento-nombre").value =
          data.nombre_evento || "";
        document.getElementById("edit-evento-descripcion").value =
          data.descripcion || "";
        document.getElementById("edit-evento-fecha").value = data.fecha || "";
        document.getElementById("edit-evento-hora-inicio").value =
          data.hora_inicio || "";
        document.getElementById("edit-evento-hora-fin").value =
          data.hora_fin || "";
        document.getElementById("edit-evento-asistentes").value =
          data.asistentes || "";

        const estadoSelect = document.getElementById("edit-evento-estado");
        for (let option of estadoSelect.options) {
          if (option.textContent === data.estado) {
            option.selected = true;
            break;
          }
        }

        document.getElementById("edit-salon-nombre").value = data.salon || "";
        document.getElementById("edit-salon-montaje").value =
          data.montaje || "";

        const btnGaurar = document.getElementById("btn-guardar-edicion");
        const estadoACtual = document.getElementById('edit-evento-estado');
        if (estadoACtual.value === 'FINAL') {
          btnGaurar.disabled = true;
          btnGaurar.textContent = "No editable (Finalizado)";
          btnGaurar.style.backgroundColor = "#6c757d";
          btnGaurar.style.cursor = "not-allowed";
          document.querySelectorAll(".btn-accion").forEach(b => b.disabled = true);
        } else {
          btnGaurar.disabled = false;
          btnGaurar.textContent = "Guardar cambios";
          btnGaurar.style.backgroundColor = "";
          btnGaurar.style.cursor = "pointer";
          document.querySelectorAll(".btn-accion").forEach(b => b.disabled = false);
        }

        valoresOriginales = {
          cliente_nombre: data.cliente.nombre || "",
          cliente_apellido_paterno: data.cliente.apellido_paterno || "",
          cliente_apellido_materno: data.cliente.apellido_materno || "",
          cliente_correo: data.cliente.correo || "",
          cliente_telefono: data.cliente.telefono || "",
          cliente_rfc: data.cliente.rfc || "",
          cliente_nombre_fiscal: data.cliente.nombre_fiscal || "",
          evento_nombre: data.nombre_evento || "",
          evento_descripcion: data.descripcion || "",
          evento_fecha: data.fecha || "",
          evento_hora_inicio: data.hora_inicio || "",
          evento_hora_fin: data.hora_fin || "",
          evento_asistentes: data.asistentes || "",
          evento_estado: data.estado || "",
        };

        document.getElementById("btn-guardar-edicion").dataset.pk = pk;

        document.getElementById("edit-servicios-list").innerHTML = "";
        document.getElementById("edit-equipos-list").innerHTML = "";
        document.getElementById("edit-mobiliarios-list").innerHTML = "";

        if (data.servicios_detalle) {
          data.servicios_detalle.forEach(servicio => {
            const id = insertarFilaEdicion("servicio");
            const selectTipo = document.getElementById(`select-tipo-${id}`);
            const selectFinal = document.getElementById(`select-final-${id}`);

            selectTipo.value = servicio.tipo_id; 
            filtrarOpciones(selectTipo, selectFinal.id, "servicio"); 
            selectFinal.value = servicio.id; 
          });
        }

        if (data.mobiliarios_detalle) {
          data.mobiliarios_detalle.forEach(mob => {
            const id = insertarFilaEdicion("mobiliario", mob.cantidad);
            const selectTipo = document.getElementById(`select-tipo-${id}`);
            const selectFinal = document.getElementById(`select-final-${id}`);

            selectTipo.value = mob.tipo_id;
            filtrarOpciones(selectTipo, selectFinal.id, "mobiliario");
            selectFinal.value = mob.id;
          });
        }

        if (data.equipos_detalle) {
          data.equipos_detalle.forEach(equipo => {
            const id = insertarFilaEdicion("equipo", equipo.cantidad);
            const selectTipo = document.getElementById(`select-tipo-${id}`);
            const selectFinal = document.getElementById(`select-final-${id}`);

            selectTipo.value = equipo.tipo_id;
            filtrarOpciones(selectTipo, selectFinal.id, "equipo");
            selectFinal.value = equipo.id;
          });
        }

        window.modalEditar.showModal();
      } catch (error) {
        console.error("Error:", error);
        mostrarToastExito("No se pudo cargar los datos para editar", "error");
      }
    });
  });

  document
    .getElementById("btn-guardar-edicion")
    .addEventListener("click", async function () {
      const pk = this.dataset.pk;
      
      const reservacionEditada = {
        nombreEvento: document.getElementById("edit-evento-nombre").value,
        descripEvento: document.getElementById("edit-evento-descripcion").value,
        fechaEvento: document.getElementById("edit-evento-fecha").value,
        horaInicio: document.getElementById("edit-evento-hora-inicio").value,
        horaFin: document.getElementById("edit-evento-hora-fin").value,
        estimaAsistentes: parseInt(document.getElementById("edit-evento-asistentes").value) || 0,
        estado_reserva: document.getElementById("edit-evento-estado").value,
      };

      reservacionEditada.reserva_servicio = [];
      document.querySelectorAll(".fila-servicio").forEach((fila) => {
        const seleccion = fila.querySelector(".item-select");
        if (seleccion && seleccion.value) {
          reservacionEditada.reserva_servicio.push({
            id: parseInt(seleccion.value)
          });
        }
      });
      reservacionEditada.reserva_equipa = [];
      document.querySelectorAll(".fila-equipo").forEach((fila) => {
        const seleccion = fila.querySelector(".item-select");
        const cantidad = fila.querySelector(".item-cantidad");
        if (seleccion && seleccion.value && cantidad && cantidad.value) {
          reservacionEditada.reserva_equipa.push({
            id: parseInt(seleccion.value),
            cantidad: parseInt(cantidad.value)
          });
        }
      });
      reservacionEditada.mobiliarios = [];
      document.querySelectorAll(".fila-mobiliario").forEach((fila) => {
        const seleccion = fila.querySelector(".item-select");
        const cantidad = fila.querySelector(".item-cantidad");
        if (seleccion && seleccion.value && cantidad && cantidad.value) {
          reservacionEditada.mobiliarios.push({
            id: parseInt(seleccion.value),
            cantidad: parseInt(cantidad.value)
          });
        }
      });

      try {
        const response = await fetch(`/api/reservacion/${pk}/`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify(reservacionEditada),
        });

        if (response.ok) {
          mostrarToastExito("Reservación actualizada", "success");
          window.modalEditar.close();
          setTimeout(() => {
            window.location.reload();
          }, 1000);
        } else {
          const errorData = await response.json();
          console.error("El backend rechazó la petición:", errorData);
          mostrarToastExito("Error al guardar: Revisa la consola", "error");
        }
      } catch (error) {
        console.error("Error:", error);
        mostrarToastExito("No se pudo conbectar al servidor", "error");
      }
    });
});

function cerrarPagos() {
  document.getElementById("modalPagos").classList.remove("mostrar");
}

function cerrarEditar() {
  window.modalEditar.close();
}
