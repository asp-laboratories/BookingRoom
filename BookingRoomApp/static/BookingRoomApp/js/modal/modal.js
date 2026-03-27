function abrirModalBEO() {
    const modal = document.getElementById("miModal");
    modal.showModal();
}

function abrirModalPagos() {
    const modal = document.getElementById("modalPagos");
    modal.showModal();
}

function cerrarModalPagos() {
    const modal = document.getElementById("modalPagos");
    modal.close();
}

function abrirBEO() {
    document.getElementById("modalBEO").style.display = "block";
}

function cerrarBEO() {
    document.getElementById("modalBEO").style.display = "none";
}

const btnAbrirModalPagos = document.getElementById('btn-abrir-modal-pagos');
if (btnAbrirModalPagos) {
    btnAbrirModalPagos.addEventListener('click', abrirModalPagos);
}

window.onclick = function(event) {
    let beo = document.getElementById("modalBEO");
    if (event.target == beo) {
        beo.style.display = "none";
    }
}

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".ver-detalles").forEach((btn) => {
      btn.addEventListener("click", async function () {
        const pk = this.dataset.pk;

        try {
          const response = await fetch(`/home/${pk}/json/`);
          if (!response.ok) throw new Error("Error al obtener datos");

          const data = await response.json();

          document.getElementById("modal-titulo-evento").textContent =
            data.nombre_evento || "Orden de banquete de evento (BEO)";

          document.getElementById("cliente-nombre").textContent =
            `${data.cliente.nombre} ${data.cliente.apellido_paterno} ${data.cliente.apellido_materno}`;
          document.getElementById("cliente-correo").textContent =
            data.cliente.correo;
          document.getElementById("cliente-telefono").textContent =
            data.cliente.telefono;
          document.getElementById("cliente-rfc").textContent = data.cliente.rfc;
          document.getElementById("cliente-nombre-fiscal").textContent =
            data.cliente.nombre_fiscal;

          document.getElementById("evento-nombre").textContent =
            data.nombre_evento;
          document.getElementById("evento-descripcion").textContent =
            data.descripcion;
          document.getElementById("evento-fecha").textContent = data.fecha;
          document.getElementById("evento-horario").textContent =
            `${data.hora_inicio} - ${data.hora_fin}`;
          document.getElementById("evento-estado").textContent = data.estado;
          document.getElementById("evento-asistentes").textContent =
            data.asistentes;

          document.getElementById("salon-nombre").textContent = data.salon;
          document.getElementById("salon-montaje").textContent = data.montaje;

          const serviciosSpan = document.getElementById("servicios-lista");
          if (data.servicios && data.servicios.length > 0) {
            serviciosSpan.textContent = data.servicios.join(", ");
          } else {
            serviciosSpan.textContent = "No hay servicios";
          }

          document.getElementById("total-iva").textContent = `$${data.iva}`;
          document.getElementById("total-subtotal").textContent =
            `$${data.subtotal}`;
          document.getElementById("total-total").textContent = `$${data.total}`;

          window.miModal.showModal();
        } catch (error) {
          console.error("Error:", error);
          alert("No se pudo cargar los detalles de la reservación");
        }
      });
    });
  });