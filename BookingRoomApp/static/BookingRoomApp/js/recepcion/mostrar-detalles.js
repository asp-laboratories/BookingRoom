
document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", async function (e) {
    const btn = e.target.closest(".ver-detalles");
    if (!btn) return;

    const pk = btn.dataset.pk;
    const idTrabajador = btn.dataset.trabajador;
    const prefix = "modal-";

    try {
      const response = await fetch(`/home/${pk}/json/`);
      if (!response.ok) throw new Error("Error al obtener datos");

      const data = await response.json();

      document.getElementById(prefix + "titulo-evento").textContent =
        data.nombre_evento || "Orden de banquete de evento (BEO)";

      document.getElementById(prefix + "cliente-nombre").textContent =
        `${data.cliente.nombre} ${data.cliente.apellido_paterno} ${data.cliente.apellido_materno}`;
      document.getElementById(prefix + "cliente-correo").textContent =
        data.cliente.correo;
      document.getElementById(prefix + "cliente-telefono").textContent =
        data.cliente.telefono;
      document.getElementById(prefix + "cliente-rfc").textContent =
        data.cliente.rfc;
      document.getElementById(prefix + "cliente-nombre-fiscal").textContent =
        data.cliente.nombre_fiscal;

      document.getElementById(prefix + "evento-nombre").textContent =
        data.nombre_evento;
      document.getElementById(prefix + "evento-descripcion").textContent =
        data.descripcion;
      document.getElementById(prefix + "evento-fecha").textContent = data.fecha;
      document.getElementById(prefix + "evento-horario").textContent =
        `${data.hora_inicio} - ${data.hora_fin}`;
      document.getElementById(prefix + "evento-estado").textContent =
        data.estado;
      document.getElementById(prefix + "evento-asistentes").textContent =
        data.asistentes;

      document.getElementById(prefix + "salon-nombre").textContent = data.salon;
      document.getElementById(prefix + "salon-montaje").textContent =
        data.montaje;

      const serviciosSpan = document.getElementById(prefix + "servicios-lista");
      if (data.servicios && data.servicios.length > 0) {
        serviciosSpan.textContent = data.servicios.join(", ");
      } else {
        serviciosSpan.textContent = "No hay servicios";
      }

      document.getElementById(prefix + "total-iva").textContent =
        `$${data.iva}`;
      document.getElementById(prefix + "total-subtotal").textContent =
        `$${data.subtotal}`;
      document.getElementById(prefix + "total-total").textContent =
        `$${data.total}`;
      const botones = document.getElementById("botones-modal");

        if (botones) {
          if (data.estado === "SOLIC" || data.estado === "Solicitud") {
            botones.style.display = "flex";
          } else {
            botones.style.display = "none";
          }
        }

        const modalElement = document.getElementById("miModal");
        if (modalElement) {
          modalElement.dataset.pk = pk;
          modalElement.dataset.trabajador = idTrabajador;
          window.miModal.showModal();
        }
    } catch (error) {
      console.error("Error:", error);
      alert("No se pudo cargar los detalles de la reservación");
    }
  });
});

// funcion para hacer el filtrado de las reservaciones de acuerdo a si se quieren solicitudes o por mas proximas
function filtrarReservaciones(evento, buscado, titulo) {
  document
    .querySelectorAll(".tab-btn")
    .forEach((boton) => boton.classList.remove("active"));
  evento.currentTarget.classList.add("active");

  document.getElementById("titulo-tab").textContent = titulo;

  const contenedro = document.getElementById("contenedor-eventos");
  const items = contenedro.querySelectorAll(".contenedor-solicitud");

  items.forEach((item) => {
    const estado = item.dataset.estado;

    if (buscado === null) {
      if (estado !== 'SOLIC') {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    } else {
      if (estado === buscado) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    }
  });
}

document.addEventListener("DOMContentLoaded", function () {
  const btnConfirmados = document.querySelector(".tab-confirm");
  if (btnConfirmados) {
    btnConfirmados.click();
  }
});
