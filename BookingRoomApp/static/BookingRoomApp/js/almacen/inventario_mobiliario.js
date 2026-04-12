function abrirModalMob(id) {
    document.getElementById('inventario_mob_id').value = id;
    
    const lista = document.getElementById('lista-resumen-mob');
    const nombreMob = document.getElementById('nombre-mob-modal');
    
    lista.innerHTML = '<li>Cargando existencias...</li>';
    nombreMob.textContent = 'Cargando...';
    
    document.getElementById('modalEstadoMob').style.display = 'block';

    fetch(`/almacen/resumen-estados-mob/${id}/`) 
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                nombreMob.textContent = data.nombre_mob;
                lista.innerHTML = ''; 
                
                let total = 0;
                data.data.forEach(item => {
                    const li = document.createElement('li');
                    li.style.marginBottom = "8px";
                    li.innerHTML = `• Estado <b>${item.estado_mobil__nombre}</b>: <span style="background:#e8f4f8; padding:2px 8px; border-radius:10px;">${item.cantidad} uds</span>`;
                    lista.appendChild(li);
                    total += item.cantidad;
                });

                const liTotal = document.createElement('li');
                liTotal.style.marginTop = "10px";
                liTotal.style.borderTop = "1px dashed #ccc";
                liTotal.style.paddingTop = "5px";
                liTotal.innerHTML = `<strong>Total físico: ${total} uds</strong>`;
                lista.appendChild(liTotal);

            } else {
                lista.innerHTML = `<li style="color:red;">Error: ${data.message}</li>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            lista.innerHTML = '<li style="color:red;">Error de conexión al obtener el resumen.</li>';
        });
}

function cerrarModalMob() {
    document.getElementById('modalEstadoMob').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('modalEstadoMob');
    if (event.target == modal) {
        cerrarModalMob();
    }
}
