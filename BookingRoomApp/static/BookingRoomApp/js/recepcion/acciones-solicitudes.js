

document.addEventListener("click", function (event) {
  const btnAceptar = event.target.closest(".js-btn-aceptar");
  const btnDenegar = event.target.closest(".js-btn-denegar");

  if (btnAceptar) {
    const pk = btnAceptar.dataset.pk;
    const idTrabajador = btnAceptar.dataset.trabajador;
    console.log("Botón Aceptar presionado. PK =", pk);

    if (pk) {
      cambiarEstadoRapido(pk, "PENDI");
    } else {
      alert("Error Técnico: El botón no recibió el ID de la reservación.");
    }
  }

  if (btnDenegar) {
    const pk = btnDenegar.dataset.pk;
    const idTrabajador = btnAceptar.dataset.trabajador;
    console.log("Botón Denegar presionado. PK =", pk);

    if (pk) {
      cambiarEstadoRapido(pk, "CANCE", idTrabajador);
    } else {
      alert("Error Técnico: El botón no recibió el ID de la reservación.");
    }
  }
});

async function cambiarEstadoRapido(pk, nuevoEstado, idTrabajador) {
  try {
    const response = await fetch(`/api/reservacion/${pk}/`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ estado_reserva: nuevoEstado, trabajador: idTrabajador}),
    });

    if (response.ok) {
      mostrarToastExito(`La solicitud fue ${nuevoEstado === 'PENDI' ? 'Aceptada' : 'Denegada'}`, "success");
      document.querySelectorAll("dialog[open]").forEach(dialog => dialog.close());
      setTimeout(() => { window.location.reload(); }, 1000);
    } else {
      console.error("Error del backend:", await response.json());
      mostrarToastExito("Error al cambiar el estado", "error");
    }
  } catch (error) {
    console.error("Error de conexión:", error);
    mostrarToastExito("No se pudo conectar con el servidor", "error");
  }
}

window.ejecutarAccionBoton = function(btoton, estado) {
    const modalPadre = btoton.closest('dialog');
    if (!modalPadre) {
        console.error("No se encontro el dialog");
        return;
    }
    const pk = modalPadre.dataset.pk;
    if (pk){
        cambiarEstadoRapido(pk, estado);
    } else {
        alert("La modal no ha cargado el id de la reservacion");
    }
}