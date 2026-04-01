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

window.onclick = function(event) {
    let pagos = document.getElementById("modalPagos");
    let beo = document.getElementById("modalBEO");

    if (event.target == pagos) {
        pagos.classList.remove("mostrar");
    }

    if (event.target == beo) {
        beo.classList.remove("mostrar");
    }
}

 document.addEventListener("DOMContentLoaded", function () {
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

          document.getElementById("beo-cliente-nombre").textContent =
            `${data.cliente.nombre} ${data.cliente.apellido_paterno} ${data.cliente.apellido_materno}`;
          document.getElementById("beo-cliente-correo").textContent =
            data.cliente.correo;
          document.getElementById("beo-cliente-telefono").textContent =
            data.cliente.telefono;
          document.getElementById("beo-cliente-rfc").textContent = data.cliente.rfc;
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

          document.getElementById("beo-total-iva").textContent = `$${data.iva}`;
          document.getElementById("beo-total-subtotal").textContent =
            `$${data.subtotal}`;
          document.getElementById("beo-total-total").textContent = `$${data.total}`;

          window.modalBEO.showModal();
        } catch (error) {
          console.error("Error:", error);
          mostrarToastExito("No se pudo cargar los detalles de la reservación", "error");
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
          document.getElementById("edit-salon-montaje").value = data.montaje || "";

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

          window.modalEditar.showModal();
        } catch (error) {
          console.error("Error:", error);
          mostrarToastExito("No se pudo cargar los datos para editar", "error");
        }
      });
    });

    document.getElementById("btn-guardar-edicion").addEventListener("click", async function () {
      const pk = this.dataset.pk;

      const valoresActuales = {
        cliente_nombre: document.getElementById("edit-cliente-nombre").value,
        cliente_apellido_paterno: document.getElementById("edit-cliente-apellido-paterno").value,
        cliente_apellido_materno: document.getElementById("edit-cliente-apellido-materno").value,
        cliente_correo: document.getElementById("edit-cliente-correo").value,
        cliente_telefono: document.getElementById("edit-cliente-telefono").value,
        cliente_rfc: document.getElementById("edit-cliente-rfc").value,
        cliente_nombre_fiscal: document.getElementById("edit-cliente-nombre-fiscal").value,
        evento_nombre: document.getElementById("edit-evento-nombre").value,
        evento_descripcion: document.getElementById("edit-evento-descripcion").value,
        evento_fecha: document.getElementById("edit-evento-fecha").value,
        evento_hora_inicio: document.getElementById("edit-evento-hora-inicio").value,
        evento_hora_fin: document.getElementById("edit-evento-hora-fin").value,
        evento_asistentes: document.getElementById("edit-evento-asistentes").value,
        evento_estado: document.getElementById("edit-evento-estado").selectedOptions[0].textContent,
      };

      const formData = new FormData();
      let hayCambios = false;

      for (const campo in valoresActuales) {
        if (valoresActuales[campo] !== valoresOriginales[campo]) {
          formData.append(campo, valoresActuales[campo]);
          hayCambios = true;
        }
      }

      if (!hayCambios) {
        mostrarToastExito("No hay cambios para guardar", "warning");
        return;
      }

      try {
        const response = await fetch(`/recepcion/historial/${pk}/actualizar/`, {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.success) {
          window.modalEditar.close();
          if (data.redirect) {
            window.location.href = data.redirect;
          }
        } else {
          mostrarToastExito(data.message, "error");
        }
      } catch (error) {
        console.error("Error:", error);
        mostrarToastExito("No se pudo guardar los cambios", "error");
      }
    });
  });

  function cerrarPagos() {
    document.getElementById("modalPagos").classList.remove("mostrar");
  }

  function cerrarEditar() {
    window.modalEditar.close();
  }