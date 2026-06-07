let aumentar = 0;
const LIMITE_CARACTERISTICAS = 4;
let valoresCaracteristicas = {};

document.addEventListener('DOMContentLoaded', function() {
    const cantidadInput = document.getElementById('cantidadCaracteristicas');
    if (cantidadInput) {
        cantidadInput.value = aumentar;
    }
});

function crearInput(numero, valorGuardado = '') {
    let nuevoDiv = document.createElement("div");
    nuevoDiv.className = "caracteristica-item";
    nuevoDiv.id = `caracteristica-${numero}`;
    
    nuevoDiv.innerHTML = `
        <label class="administrador-label">Característica ${numero}:
            <input class="administrador-input" type="text" 
                name="caracteristica_${numero}" 
                placeholder="Descripción de característica" 
                value="${valorGuardado}" required />
        </label>
    `;
    
    document.getElementById("contenedor-caracteristicas").appendChild(nuevoDiv);
}

function guardarValoresActuales() {
    for (let i = 1; i <= aumentar; i++) {
        const input = document.querySelector(`input[name="caracteristica_${i}"]`);
        if (input) {
            valoresCaracteristicas[i] = input.value;
        }
    }
}

function restaurarValores() {
    for (let i = 1; i <= aumentar; i++) {
        if (valoresCaracteristicas[i]) {
            crearInput(i, valoresCaracteristicas[i]);
        }
    }
}

function disminuirTotalInputs(event) {
    if (aumentar > 0) {
        guardarValoresActuales();
        delete valoresCaracteristicas[aumentar];
        aumentar -= 1;
        document.getElementById("contenedor-caracteristicas").innerHTML = "";
        for (let i = 1; i <= aumentar; i++) {
            let valor = valoresCaracteristicas[i] || '';
            crearInput(i, valor);
        }
        document.getElementById('cantidadCaracteristicas').value = aumentar;
    }
}

function aumentarTotalInputs(event) {
    if (aumentar >= LIMITE_CARACTERISTICAS) {
        alert(`Máximo ${LIMITE_CARACTERISTICAS} características permitidas`);
        return;
    }
    
    guardarValoresActuales();
    aumentar += 1;
    crearInput(aumentar, '');
    document.getElementById('cantidadCaracteristicas').value = aumentar;
}
