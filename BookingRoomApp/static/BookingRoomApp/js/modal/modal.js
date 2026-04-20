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
          document.getElementById(prefix + "cliente-rfc").textContent = data.cliente.rfc;
          document.getElementById(prefix + "cliente-nombre-fiscal").textContent =
            data.cliente.nombre_fiscal;

          document.getElementById(prefix + "evento-nombre").textContent =
            data.nombre_evento;
          document.getElementById(prefix + "evento-descripcion").textContent =
            data.descripcion;
          document.getElementById(prefix + "evento-fecha").textContent = data.fecha;
          document.getElementById(prefix + "evento-horario").textContent =
            `${data.hora_inicio} - ${data.hora_fin}`;
          document.getElementById(prefix + "evento-estado").textContent = data.estado;
          document.getElementById(prefix + "evento-asistentes").textContent =
            data.asistentes;

          document.getElementById(prefix + "salon-nombre").textContent = data.salon;
          document.getElementById(prefix + "salon-costo").textContent = data.salon_costo ? `$${data.salon_costo}` : '-';
          document.getElementById(prefix + "salon-montaje").textContent = data.montaje;

          const serviciosSpan = document.getElementById(prefix + "servicios-lista");
          if (data.servicios && data.servicios.length > 0) {
            serviciosSpan.innerHTML = data.servicios.map(s => `<span class="item-lista">• ${s.nombre} - $${s.costo}</span>`).join('');
          } else {
            serviciosSpan.textContent = "No hay servicios";
          }

          document.getElementById(prefix + "total-iva").textContent = `$${data.iva}`;
          document.getElementById(prefix + "total-subtotal").textContent =
            `$${data.subtotal}`;
          document.getElementById(prefix + "total-total").textContent = `$${data.total}`;

          window.miModal.showModal();
        } catch (error) {
          console.error("Error:", error);
          alert("No se pudo cargar los detalles de la reservación");
        }
      });
    });
  });