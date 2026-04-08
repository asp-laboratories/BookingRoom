async function abrirModalDetalleCompleto(pk) {
  const prefix = "detalle-";

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
      data.descripcion || "Sin descripción";
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

    const equipamientosSpan = document.getElementById(prefix + "equipamientos-lista");
    if (data.equipamientos && data.equipamientos.length > 0) {
      equipamientosSpan.textContent = data.equipamientos.join(", ");
    } else {
      equipamientosSpan.textContent = "No hay equipamientos";
    }

    document.getElementById(prefix + "total-iva").textContent = `$${data.iva}`;
    document.getElementById(prefix + "total-subtotal").textContent =
      `$${data.subtotal}`;
    document.getElementById(prefix + "total-total").textContent = `$${data.total}`;

    document.getElementById('modalDetalleCompleto').showModal();
  } catch (error) {
    console.error("Error:", error);
    alert("No se pudo cargar los detalles de la reservación");
  }
}

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

      // Ocultar botones si el estado es confirmado (ya no se puede aceptar/rechazar)
      const contenedorBotones = document.querySelector('.modal-botones');
      const estadoReservacion = data.estado;
      const estadosSinBotones = ['Confirmada', 'Pagada', 'Finalizada', 'Cancelada'];
      
      if (contenedorBotones) {
        if (estadosSinBotones.includes(estadoReservacion)) {
          contenedorBotones.style.display = 'none';
        } else {
          contenedorBotones.style.display = 'flex';
        }
      }

      window.miModal.showModal();
    } catch (error) {
      console.error("Error:", error);
      alert("No se pudo cargar los detalles de la reservación");
    }
  });
});