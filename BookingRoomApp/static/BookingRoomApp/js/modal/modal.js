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
