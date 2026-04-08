document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.ver-detalles-solicitud').forEach(btn => {
        btn.addEventListener('click', function() {
            const pk = this.dataset.pk;
            if (typeof cargarDetallesSolicitud === 'function') {
                cargarDetallesSolicitud(pk);
            }
        });
    });
});
