
function datosReservacion() {
  // id del cliente y trabajador
  const cliente = document.getElementById("cliente-rfc")?.value;
  if (!cliente) {
    mostrarToastExito("Cliente no localizado", "error");
    return null;
  }

  const trabajador = document.getElementById("trabajador_id").value;
  if (!trabajador) {
    mostrarToastExito("No se identifico al trabajador", "error");
    return null;
  }

  // Reservacion info
  const nombre = document.getElementById("nombreEvento")?.value?.trim();
  const tipo_evento = document.getElementById("tipo_evento")?.value;
  const fechaEvento = document.getElementById("fecha_evento")?.value;
  const estimaAsistentes = document.getElementById(
    "estimado_asistentes",
  )?.value;
  const horaInicio = document.getElementById("hora_inicio")?.value;
  const horaFin = document.getElementById("hora_fin")?.value;
  const descripEvento = document
    .getElementById("descripcion_evento")
    ?.value?.trim();

  if (
    !nombre ||
    !tipo_evento ||
    !fechaEvento ||
    !estimaAsistentes ||
    !horaInicio ||
    !horaFin ||
    !descripEvento
  ) {
    mostrarToastExito("Datos faltantes de reservacion", "error");
    return null;
  }

  // montaje/salon/mobiliario
  const salon = document.getElementById("select-salon")?.value;
  const tipo_montaje = document.getElementById("select-montaje")?.value;

  const mobiliarios = [];
  document.querySelectorAll(".mobil-pair").forEach((pair) => {
    const mobiliarioSeleccionado = pair.querySelector(".mobiliario-select");
    const cantidad = pair.querySelector('input[type="number"]');

    if (
      mobiliarioSeleccionado &&
      mobiliarioSeleccionado.value &&
      cantidad &&
      cantidad.value
    ) {
      mobiliarios.push({
        id: mobiliarioSeleccionado.value,
        cantidad: parseInt(cantidad.value),
      });
    } else {
      mostrarToastExito("Datos de mobiliario incompletos", "error");
      return null;
    }
  });

  if (!salon || !tipo_montaje) {
    mostrarToastExito(
      "No se han completado los campos de salon y montaje",
      "error",
    );
    return null;
  }

  montaje = {
    salon: parseInt(salon),
    tipo_montaje: parseInt(tipo_montaje),
    mobiliarios,
  };

  // servicios
  const reserva_servicio = [];
  document.querySelectorAll(".servicio-select").forEach((pair) => {
    if (pair.value) {
      reserva_servicio.push({ id: parseInt(pair.value) });
    }
  });

  // equipamientos
  const reserva_equipa = [];
  document.querySelectorAll(".equipo-pair").forEach((pair) => {
    const equipamiento = pair.querySelector(".equipamiento-select");
    const cantidad = pair.querySelector('input[type="number"]');

    if (equipamiento && cantidad && equipamiento.value && cantidad.value) {
      reserva_equipa.push({
        id: parseInt(equipamiento.value),
        cantidad: parseInt(cantidad.value),
      });
    }
  });

  // armao del json q se enviara
  return {
    nombre: nombre,
    descripEvento: descripEvento,
    estimaAsistentes: parseInt(estimaAsistentes),
    fechaEvento: fechaEvento,
    horaInicio: horaInicio,
    horaFin: horaFin,
    cliente: cliente,
    trabajador: trabajador,
    reserva_servicio: reserva_servicio,
    reserva_equipa: reserva_equipa,
    montaje: montaje,
    tipo_evento: parseInt(tipo_evento),
  };
}

function otenerError(info) {
  if (info.error) return info.error;
  if (typeof info === "object") {
    for (const key in info) {
      const val = info[key];
      if (Array.isArray(val)) return `${key}: ${val[0]}`;
      if (typeof val === "string") return `${key}: ${val}`;
    }
  }
  return "No se localizo el error";
}

async function crearReservacion() {
  const datos = datosReservacion();

  if (!datos) return;

  try {
    const respuesta = await fetch("/api/reservacion/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(datos),
    });

    const data = await respuesta.json();

    if (respuesta.ok) {
      mostrarToastExito("Reservacion creada con exito", "success");
      const modalPago = document.getElementById("modalPagos");
      const reservacion_id = modalPago.querySelector(
        '[data-field="reservacion"]',
      );
      if (reservacion_id) {
        reservacion_id.value = data.id;
      }
      modalPago.showModal();
    } else {
      const errro = otenerError(data);
      mostrarToastExito(`Error: ${errro}`, "error");
      console.error("Error API:", data);
    }
  } catch (error) {
    mostrarToastExito("Error en la conexion con el servidor", "error");
    console.error(error);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const botonReservacion = document.querySelector(".reservacion-btn-confirmar");
  if (botonReservacion) {
    botonReservacion.onclick = function () {
      abrirModalConfirmar(
        "Confirmar reservacion",
        "¿Estas seguro de realizar esta reservacion?",
        crearReservacion,
      );
    };
  }
});
