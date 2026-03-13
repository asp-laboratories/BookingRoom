function abrirPagos() {
    document.getElementById("modalPagos").style.display = "block";
}

function cerrarPagos() {
    document.getElementById("modalPagos").style.display = "none";
}

function abrirBEO() {
    document.getElementById("modalBEO").style.display = "block";
}

function cerrarBEO() {
    document.getElementById("modalBEO").style.display = "none";
}

window.onclick = function(event) {

    let pagos = document.getElementById("modalPagos");
    let beo = document.getElementById("modalBEO");

    if (event.target == pagos) {
        pagos.style.display = "none";
    }

    if (event.target == beo) {
        beo.style.display = "none";
    }
}
