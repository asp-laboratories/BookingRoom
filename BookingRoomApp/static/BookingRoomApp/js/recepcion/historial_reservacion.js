function abrirPagos() {
    document.getElementById("modalPagos").classList.add("mostrar");
}

function cerrarPagos() {
    document.getElementById("modalPagos").classList.remove("mostrar");
}

function cerrarEditar() {
    document.getElementById("modalEditar").close();
}

function cerrarDetalleCompleto() {
    document.getElementById("modalDetalleCompleto").close();
}

function cerrarEditar() {
    window.modalEditar.close();
}

function cambiarTab(tab) {
    const url = new URL(window.location.href);
    url.searchParams.set('tab', tab);
    window.location.href = url.toString();
}

function cerrarEditarCliente() {
    document.getElementById("modalEditarCliente").close();
}

let clienteOriginales = {};

async function abrirEditarCliente(pk) {
    try {
        const response = await fetch(`/api/datos-cliente/${pk}/`);
        if (!response.ok) throw new Error("Error al obtener datos");

        const data = await response.json();

        document.getElementById("edit-cliente-id").value = data.id;
        document.getElementById("edit-cliente-nombre").value = data.nombre || "";
        document.getElementById("edit-cliente-apellido-paterno").value = data.apellidoPaterno || "";
        document.getElementById("edit-cliente-apellido-materno").value = data.apelidoMaterno || "";
        document.getElementById("edit-cliente-correo").value = data.correo_electronico || "";
        document.getElementById("edit-cliente-telefono").value = data.telefono || "";
        document.getElementById("edit-cliente-rfc").value = data.rfc || "";
        document.getElementById("edit-cliente-nombre-fiscal").value = data.nombre_fiscal || "";

        const tipoSelect = document.getElementById("edit-cliente-tipo");
        for (let option of tipoSelect.options) {
            if (option.value === data.tipo_cliente_codigo) {
                option.selected = true;
                break;
            }
        }

        clienteOriginales = {
            nombre: data.nombre || "",
            apellidoPaterno: data.apellidoPaterno || "",
            apelidoMaterno: data.apelidoMaterno || "",
            correo: data.correo_electronico || "",
            telefono: data.telefono || "",
            rfc: data.rfc || "",
            nombreFiscal: data.nombre_fiscal || "",
            tipo: data.tipo_cliente_codigo || ""
        };

        document.getElementById("modalEditarCliente").showModal();
    } catch (error) {
        console.error("Error:", error);
        mostrarToastExito("No se pudieron cargar los datos del cliente", "error");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".editar-cliente-btn").forEach(function(btn) {
        btn.addEventListener("click", function(e) {
            e.stopPropagation();
            const pk = this.dataset.pk;
            abrirEditarCliente(pk);
        });
    });

    document.querySelectorAll(".cliente-row").forEach(function(row) {
        row.addEventListener("click", function() {
            const pk = this.dataset.pk;
            abrirEditarCliente(pk);
        });
    });

    var btnGuardarCliente = document.getElementById("btn-guardar-cliente");
    if (btnGuardarCliente) {
        btnGuardarCliente.addEventListener("click", async function() {
            var clienteId = document.getElementById("edit-cliente-id").value;

            var valoresActuales = {
                nombre: document.getElementById("edit-cliente-nombre").value,
                apellidoPaterno: document.getElementById("edit-cliente-apellido-paterno").value,
                apelidoMaterno: document.getElementById("edit-cliente-apellido-materno").value,
                correo: document.getElementById("edit-cliente-correo").value,
                telefono: document.getElementById("edit-cliente-telefono").value,
                rfc: document.getElementById("edit-cliente-rfc").value,
                nombre_fiscal: document.getElementById("edit-cliente-nombre-fiscal").value,
                tipo_cliente: document.getElementById("edit-cliente-tipo").value
            };

            var formData = new FormData();
            formData.append("cliente_id", clienteId);

            for (var campo in valoresActuales) {
                formData.append(campo, valoresActuales[campo]);
            }

            try {
                var response = await fetch("/recepcion/historial/", {
                    method: "POST",
                    body: formData
                });

                var data = await response.json();

                if (data.success) {
                    mostrarToastExito(data.message, "success");
                    document.getElementById("modalEditarCliente").close();
                    setTimeout(function() {
                        window.location.reload();
                    }, 1000);
                } else {
                    mostrarToastExito(data.message, "error");
                }
            } catch (error) {
                console.error("Error:", error);
                mostrarToastExito("No se pudieron guardar los cambios", "error");
            }
        });
    }
});

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
            
            document.getElementById('detalle-titulo-evento').textContent = data.nombre_evento || "Evento";
            
            document.getElementById('detalle-cliente-nombre').textContent = 
                `${data.cliente?.nombre || '-'} ${data.cliente?.apellido_paterno || ''} ${data.cliente?.apellido_materno || ''}`.trim();
            document.getElementById('detalle-cliente-correo').textContent = data.cliente?.correo || '-';
            document.getElementById('detalle-cliente-telefono').textContent = data.cliente?.telefono || '-';
            document.getElementById('detalle-cliente-rfc').textContent = data.cliente?.rfc || '-';
            document.getElementById('detalle-cliente-nombre-fiscal').textContent = data.cliente?.nombre_fiscal || '-';
            
            document.getElementById('detalle-evento-nombre').textContent = data.nombre_evento || '-';
            document.getElementById('detalle-evento-descripcion').textContent = data.descripcion || '-';
            document.getElementById('detalle-evento-fecha').textContent = data.fecha || '-';
            document.getElementById('detalle-evento-horario').textContent = 
                `${data.hora_inicio || '-'} - ${data.hora_fin || '-'}`;
            document.getElementById('detalle-evento-estado').textContent = data.estado || '-';
            document.getElementById('detalle-evento-asistentes').textContent = data.asistentes || '-';
            
            document.getElementById('detalle-salon-nombre').textContent = data.salon || '-';
            document.getElementById('detalle-salon-montaje').textContent = data.montaje || '-';
            
            const serviciosSpan = document.getElementById('detalle-servicios-lista');
            if (data.servicios && data.servicios.length > 0) {
                serviciosSpan.innerHTML = data.servicios.map(s => `<span class="item-lista">• ${s}</span>`).join('');
            } else {
                serviciosSpan.textContent = 'No hay servicios';
            }

            // Mobiliarios
            const mobiliariosSpan = document.getElementById('detalle-mobiliario-lista');
            if (mobiliariosSpan && data.mobiliarios && data.mobiliarios.length > 0) {
                mobiliariosSpan.innerHTML = data.mobiliarios.map(m => `<span class="item-lista">• ${m.nombre} (x${m.cantidad})</span>`).join('');
            } else if (mobiliariosSpan) {
                mobiliariosSpan.textContent = 'No hay mobiliarios';
            }

            // Equipamientos
            const equipamientosSpan = document.getElementById('detalle-equipamientos-lista');
            if (equipamientosSpan && data.equipamentos && data.equipamentos.length > 0) {
                equipamientosSpan.innerHTML = data.equipamentos.map(e => `<span class="item-lista">• ${e.nombre} (x${e.cantidad})</span>`).join('');
            } else if (equipamientosSpan) {
                equipamientosSpan.textContent = 'No hay equipamientos';
            }
            
            document.getElementById('detalle-total-iva').textContent = `$${data.iva || '0.00'}`;
            document.getElementById('detalle-total-subtotal').textContent = `$${data.subtotal || '0.00'}`;
            document.getElementById('detalle-total-total').textContent = `$${data.total || '0.00'}`;
            
            document.getElementById('modalDetalleCompleto').showModal();
        } catch (error) {
            console.error("Error:", error);
            mostrarToastExito('No se pudo cargar los detalles', 'error');
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

          document.getElementById("edit-evento-nombre").value =
            data.nombre_evento || "";
          document.getElementById("edit-evento-descripcion").value =
            data.descripcion || "";

          valoresOriginales = {
            evento_nombre: data.nombre_evento || "",
            evento_descripcion: data.descripcion || "",
          };

          document.getElementById("btn-guardar-edicion").dataset.pk = pk;
          document.getElementById("btn-cancelar-reservacion").dataset.pk = pk;

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
        evento_nombre: document.getElementById("edit-evento-nombre").value,
        evento_descripcion: document.getElementById("edit-evento-descripcion").value,
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
    document.getElementById("modalEditar").close();
}

async function abrirModalDetalleCompleto(pk) {
    try {
        const response = await fetch(`/home/${pk}/json/`);
        if (!response.ok) throw new Error("Error al obtener datos");
        
        const data = await response.json();
        
        document.getElementById('detalle-titulo-evento').textContent = data.nombre_evento || "Evento";
        
        document.getElementById('detalle-cliente-nombre').textContent = 
            `${data.cliente?.nombre || '-'} ${data.cliente?.apellido_paterno || ''} ${data.cliente?.apellido_materno || ''}`.trim();
        document.getElementById('detalle-cliente-correo').textContent = data.cliente?.correo || '-';
        document.getElementById('detalle-cliente-telefono').textContent = data.cliente?.telefono || '-';
        document.getElementById('detalle-cliente-rfc').textContent = data.cliente?.rfc || '-';
        document.getElementById('detalle-cliente-nombre-fiscal').textContent = data.cliente?.nombre_fiscal || '-';
        
        document.getElementById('detalle-evento-nombre').textContent = data.nombre_evento || '-';
        document.getElementById('detalle-evento-descripcion').textContent = data.descripcion || '-';
        document.getElementById('detalle-evento-fecha').textContent = data.fecha || '-';
        document.getElementById('detalle-evento-horario').textContent = 
            `${data.hora_inicio || '-'} - ${data.hora_fin || '-'}`;
        document.getElementById('detalle-evento-estado').textContent = data.estado || '-';
        document.getElementById('detalle-evento-asistentes').textContent = data.asistentes || '-';
        
        document.getElementById('detalle-salon-nombre').textContent = data.salon || '-';
        document.getElementById('detalle-salon-montaje').textContent = data.montaje || '-';
        
        const serviciosSpan = document.getElementById('detalle-servicios-lista');
        if (data.servicios && data.servicios.length > 0) {
            serviciosSpan.innerHTML = data.servicios.map(s => `<span class="item-lista">• ${s}</span>`).join('');
        } else {
            serviciosSpan.textContent = 'No hay servicios';
        }
        
        document.getElementById('detalle-equipamientos-lista').textContent = 'No hay equipamientos';
        
        document.getElementById('detalle-total-iva').textContent = `$${data.iva || '0.00'}`;
        document.getElementById('detalle-total-subtotal').textContent = `$${data.subtotal || '0.00'}`;
        document.getElementById('detalle-total-total').textContent = `$${data.total || '0.00'}`;
        
        document.getElementById('modalDetalleCompleto').showModal();
    } catch (error) {
        console.error("Error:", error);
        mostrarToastExito('No se pudo cargar los detalles', 'error');
    }
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
        abrirModalDetalleCompleto(pk);
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

          document.getElementById("edit-evento-nombre").value =
            data.nombre_evento || "";
          document.getElementById("edit-evento-descripcion").value =
            data.descripcion || "";

          valoresOriginales = {
            evento_nombre: data.nombre_evento || "",
            evento_descripcion: data.descripcion || "",
          };

          document.getElementById("btn-guardar-edicion").dataset.pk = pk;
          document.getElementById("btn-cancelar-reservacion").dataset.pk = pk;

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
        evento_nombre: document.getElementById("edit-evento-nombre").value,
        evento_descripcion: document.getElementById("edit-evento-descripcion").value,
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

document.getElementById("btn-cancelar-reservacion")?.addEventListener("click", async function () {
    const pk = this.dataset.pk;
    if (!pk) return;

    if (!confirm("¿Estás seguro de cancelar esta reservación? Se liberarán el salón, mobiliario, equipamiento y servicios asignados.")) {
        return;
    }

    try {
        const response = await fetch(`/home/${pk}/cancelar/`, {
            method: "POST",
        });

        const data = await response.json();

        if (data.success) {
            mostrarToastExito(data.message, "success");
            window.modalEditar.close();
            setTimeout(() => window.location.reload(), 1500);
        } else {
            mostrarToastExito(data.message, "error");
        }
    } catch (error) {
        console.error("Error:", error);
        mostrarToastExito("No se pudo cancelar la reservación", "error");
    }
});