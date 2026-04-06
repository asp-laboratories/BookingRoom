
document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", async function (e) {
    const btn = e.target.closest(".ver-detalles");
    if (!btn) return;
    
    const pk = btn.dataset.pk;
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
      document.getElementById(prefix + "salon-montaje").textContent = data.montaje;

      const serviciosSpan = document.getElementById(prefix + "servicios-lista");
      if (data.servicios && data.servicios.length > 0) {
        serviciosSpan.textContent = data.servicios.join(", ");
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

// funcion para hacer filtrado chido por fecha
function filtrarRecientes() {
  const contenedor = document.getElementById('contenedor-eventos');
  const items = Array.from(contenedor.querySelectorAll('.contenedor-solicitud'));

  items.forEach(item => item.style.display = '');

  items.sort((a, b) => {
    const fecha_1 = new Date(a.dataset.fecha || 0);
    const fecha_2 = new Date(b.dataset.fecha || 0);
    return fecha_2 - fecha_1;
  });

  items.forEach(item => contenedor.appendChild(item));

}

// funcion para hacer filtrado chido po estado
function filtrarSolicitudes() {
  const contenedor = document.getElementById('contenedor-eventos');
  const items = contenedor.querySelectorAll('.contenedor-solicitud');

  items.forEach(item => {
    if (!estado || item.dataset.estado === 'SOLIC') {
      item.style.display = '';
    } else {
      item.style.display = 'none';
    }
  });

}
