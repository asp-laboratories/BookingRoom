function abrirModal(id) {
    document.getElementById("inventario_id").value = id;
    document.getElementById("modalEstado").style.display = "block";
}

function cerrarModal() {
    document.getElementById("modalEstado").style.display = "none";
}

window.onclick = function(event) {
    let modal = document.getElementById("modalEstado");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
