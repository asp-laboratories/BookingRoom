console.log('=== inventario_equipamiento.js cargado ===');

function abrirModal(id) {
    console.log('=== abrirModal llamado ===');
    console.log('ID:', id);
    
    const modal = document.getElementById('modalEstado');
    console.log('Modal element:', modal);
    
    if (!modal) {
        console.error('Modal no encontrado!');
        alert('Error: Modal no encontrado');
        return;
    }
    
    document.getElementById('inventario_id').value = id;

    const lista = document.getElementById('lista-resumen');
    const nombreEquipo = document.getElementById('nombre-equipo-modal');

    lista.innerHTML = '<li>Cargando existencias...</li>';
    nombreEquipo.textContent = 'Cargando...';

    modal.style.display = 'block';
    console.log('Modal abierto');

    const url = `/almacen/resumen-estados/${id}/`;
    console.log('Fetching:', url);
    
    fetch(url)
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            if (data.status === 'success') {
                nombreEquipo.textContent = data.nombre_equipo;
                
                lista.innerHTML = ''; 
                
                let total = 0;
                data.data.forEach(item => {
                    const li = document.createElement('li');
                    li.style.marginBottom = "8px";
                    li.innerHTML = `• Estado <b>${item.estado_equipa__nombre}</b>: <span style="background:#e8f4f8; padding:2px 8px; border-radius:10px;">${item.cantidad} uds</span>`;
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

function cerrarModal() {
    document.getElementById('modalEstado').style.display = 'none';
}

// Cerrar modal al hacer clic fuera de él
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modalEstado');
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                cerrarModal();
            }
        });
    }
});
