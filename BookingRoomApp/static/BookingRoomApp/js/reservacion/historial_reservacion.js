function abrirPagos() {
    document.getElementById("modalPagos").classList.add("mostrar");
}

function cerrarPagos() {
    document.getElementById("modalPagos").classList.remove("mostrar");
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
