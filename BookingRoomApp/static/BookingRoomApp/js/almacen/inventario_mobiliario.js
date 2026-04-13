function abrirModalMob(id) {
    console.log('=== abrirModalMob llamado ===');
    console.log('ID:', id);
    
    const modal = document.getElementById('modalEstadoMob');
    console.log('Modal element:', modal);
    
    if (!modal) {
        console.error('Modal no encontrado!');
        alert('Error: Modal no encontrado');
        return;
    }
    
    document.getElementById('inventario_mob_id').value = id;

    const lista = document.getElementById('lista-resumen-mob');
    const nombreMob = document.getElementById('nombre-mob-modal');

    lista.innerHTML = '<li>Cargando existencias...</li>';
    nombreMob.textContent = 'Cargando...';

    modal.style.display = 'block';
    console.log('Modal abierto');

    const url = `/almacen/resumen-estados-mob/${id}/`;
    console.log('Fetching:', url);
    
    fetch(url)
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
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

// Cerrar modal al hacer clic fuera de él
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modalEstadoMob');
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                cerrarModalMob();
            }
        });
    }
});
