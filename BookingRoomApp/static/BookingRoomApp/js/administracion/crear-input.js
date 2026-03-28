let aumentar = 0;

document.addEventListener('DOMContentLoaded', function() {
    const cantidadInput = document.getElementById('cantidadCaracteristicas');
    if (cantidadInput) {
        cantidadInput.value = aumentar;
    }
});

function crearInput(numero) {
    let nuevoDiv = document.createElement("div");
    nuevoDiv.className = "caracteristica-item";
    nuevoDiv.id = `caracteristica-${numero}`;
    
    nuevoDiv.innerHTML = `
        <label class="administrador-label">Característica ${numero}:
            <input class="administrador-input" type="text" 
                name="caracteristica_${numero}" 
                placeholder="Descripción de característica" required />
        </label>
    `;
    
    document.getElementById("contenedor-caracteristicas").appendChild(nuevoDiv);
}

function disminuirTotalInputs(event) {

    
    if (aumentar > 0) {
        aumentar -= 1;
        document.getElementById("contenedor-caracteristicas").innerHTML = "";
        for (let i = 1; i <= aumentar; i++) {
            crearInput(i);
        }
        document.getElementById('cantidadCaracteristicas').value = aumentar;
    }
}

function aumentarTotalInputs(event) {

    
    aumentar += 1;
    crearInput(aumentar);
    document.getElementById('cantidadCaracteristicas').value = aumentar;
}
