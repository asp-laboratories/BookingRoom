function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

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

    document.getElementById(prefix + "salon-nombre").textContent = `${data.salon} ($${data.salon_costo || '0.00'})`;
    document.getElementById(prefix + "salon-montaje").textContent = data.montaje;

    const serviciosSpan = document.getElementById(prefix + "servicios-lista");
    if (data.servicios && data.servicios.length > 0) {
      serviciosSpan.innerHTML = data.servicios.map(s => `<span class="item-lista"> • ${s.nombre} - $${s.costo} </span>`).join('');
    } else {
      serviciosSpan.textContent = "No hay servicios";
    }

    const equipamentosSpan = document.getElementById(prefix + "equipamientos-lista");
    if (data.equipamentos && data.equipamentos.length > 0) {
      equipamentosSpan.innerHTML = data.equipamentos.map(e => `<span class="item-lista"> • ${e.nombre} (${e.cantidad}) - $${e.costo} </span>`).join('');
    } else {
      equipamentosSpan.textContent = "No hay equipamientos";
    }

    const mobiliarioSpan = document.getElementById(prefix + "mobiliario-lista");
    if (data.mobiliarios && data.mobiliarios.length > 0) {
      mobiliarioSpan.innerHTML = data.mobiliarios.map(m => `<span class="item-lista"> • ${m.nombre} (${m.cantidad}) - $${m.costo} WS</span>`).join('');
    } else {
      mobiliarioSpan.textContent = "No hay mobiliario";
    }

    const descripcionInput = document.getElementById("modal-evento-descripcion-input");
    if (descripcionInput) {
      descripcionInput.value = data.descripcion || "";
    }

    document.getElementById(prefix + "total-iva").textContent = `$${data.iva}`;
    document.getElementById(prefix + "total-subtotal").textContent =
      `$${data.subtotal}`;
    document.getElementById(prefix + "total-total").textContent = `$${data.total}`;

    document.getElementById('modalDetalleCompleto').dataset.reservacionId = pk;
    document.getElementById('modalDetalleCompleto').dataset.estadoActual = data.estado_codigo;

    document.getElementById('modalDetalleCompleto').showModal();
  } catch (error) {
    console.error("Error:", error);
    alert("No se pudo cargar los detalles de la reservación");
  }
}

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
      data.descripcion || "Sin descripción";
    document.getElementById(prefix + "evento-fecha").textContent = data.fecha;
    document.getElementById(prefix + "evento-horario").textContent =
      `${data.hora_inicio} - ${data.hora_fin}`;
    document.getElementById(prefix + "evento-estado").textContent = data.estado;
    document.getElementById(prefix + "evento-asistentes").textContent =
      data.asistentes;

    document.getElementById(prefix + "salon-nombre").textContent = `${data.salon} ($${data.salon_costo || '0.00'})`;
    document.getElementById(prefix + "salon-montaje").textContent = data.montaje;

    const serviciosSpan = document.getElementById(prefix + "servicios-lista");
    if (data.servicios && data.servicios.length > 0) {
      serviciosSpan.innerHTML = data.servicios.map(s => `<span class="item-lista">• ${s.nombre} - $${s.costo}</span>`).join('');
    } else {
      serviciosSpan.textContent = "No hay servicios";
    }

    const equipamientosSpan = document.getElementById(prefix + "equipamientos-lista");
    if (data.equipamentos && data.equipamentos.length > 0) {
      equipamientosSpan.innerHTML = data.equipamentos.map(e => `<span class="item-lista">• ${e.nombre} (${e.cantidad}) - $${e.costo}</span>`).join('');
    } else {
      equipamientosSpan.textContent = "No hay equipamientos";
    }

    const mobiliarioSpan = document.getElementById(prefix + "mobiliario-lista");
    if (data.mobiliarios && data.mobiliarios.length > 0) {
      mobiliarioSpan.innerHTML = data.mobiliarios.map(m => `<span class="item-lista">• ${m.nombre} (${m.cantidad}) - $${m.costo}</span>`).join('');
    } else {
      mobiliarioSpan.textContent = "No hay mobiliario";
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
});

// Funciones para confirmar y cancelar reservaciones
async function abrirConfirmarModal(pk, descripcion) {
  document.getElementById('modal-confirmar-titulo').textContent = 'Confirmar Reservación';
  document.getElementById('modal-confirmar-mensaje').textContent = '¿Estás seguro de que quieres confirmar esta reservación? El trabajador actual será asignado como responsable.';
  document.getElementById('modal-confirmar-btn').onclick = function() {
    confirmarReservacion(pk, descripcion);
  };
  document.getElementById('modal-confirmar').showModal();
}

async function abrirCancelarModal(pk) {
  document.getElementById('modal-cancelar-titulo').textContent = 'Cancelar Reservación';
  document.getElementById('modal-cancelar-mensaje').textContent = '¿Estás seguro de que quieres cancelar esta reservación? Esta acción no se puede deshacer.';
  document.getElementById('modal-cancelar-btn').onclick = function() {
    cancelarReservacion(pk);
  };
  document.getElementById('modal-cancelar').showModal();
}

async function confirmarReservacion(pk, descripcion) {
  try {
    const formData = new FormData();
    formData.append('descripcion', descripcion);
    
    const response = await fetch(`/home/${pk}/confirmar/`, {
      method: 'POST',
      body: formData,
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    });
    
    const data = await response.json();
    
    if (data.success) {
      alert('Reservación confirmada correctamente');
      document.getElementById('modal-confirmar').close();
      document.getElementById('miModal').close();
      location.reload();
    } else {
      alert('Error: ' + data.message);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('No se pudo confirmar la reservación');
  }
}

async function cancelarReservacion(pk) {
  try {
    const response = await fetch(`/home/${pk}/cancelar/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken')
      }
    });
    
    const data = await response.json();
    
    if (data.success) {
      alert('Reservación cancelada correctamente');
      document.getElementById('modal-cancelar').close();
      document.getElementById('miModal').close();
      location.reload();
    } else {
      alert('Error: ' + data.message);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('No se pudo cancelar la reservación');
  }
}

function cerrarModalConfirmar() {
  document.getElementById('modal-confirmar').close();
}

function cerrarModalCancelar() {
  document.getElementById('modal-cancelar').close();
}

function abrirConfirmarModalDesdeDetalle() {
  const modal = document.getElementById('modalDetalleCompleto');
  const pk = modal.dataset.reservacionId;
  const descripcion = document.getElementById("modal-evento-descripcion-input").value;
  if (pk) {
    abrirConfirmarModal(pk, descripcion);
  }
}

function abrirCancelarModalDesdeDetalle() {
  const modal = document.getElementById('modalDetalleCompleto');
  const pk = modal.dataset.reservacionId;
  if (pk) {
    abrirCancelarModal(pk);
  }
}