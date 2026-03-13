function abrirModalBEO() {
    const modal = document.getElementById("miModal");
    modal.showModal();
}

function abrirBEO() {
    document.getElementById("modalBEO").style.display = "block";
}

function cerrarBEO() {
    document.getElementById("modalBEO").style.display = "none";
}

window.onclick = function(event) {
    let beo = document.getElementById("modalBEO");
    if (event.target == beo) {
        beo.style.display = "none";
    }
}
