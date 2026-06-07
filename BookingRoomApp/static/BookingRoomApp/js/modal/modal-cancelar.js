let callbackCancelar = null;

function abrirModalCancelar(titulo, mensaje, callback) {
    document.getElementById('modal-cancelar-titulo').textContent = titulo || 'Cancelar acción';
    document.getElementById('modal-cancelar-mensaje').textContent = mensaje || '¿Estás seguro de que quieres cancelar?';
    callbackCancelar = callback;
    document.getElementById('modal-cancelar').showModal();
}

function cerrarModalCancelar() {
    document.getElementById('modal-cancelar').close();
    callbackCancelar = null;
}

document.addEventListener('DOMContentLoaded', function() {
    const cancelarBtn = document.getElementById('modal-cancelar-btn');
    if (cancelarBtn) {
        cancelarBtn.addEventListener('click', function() {
            if (callbackCancelar && typeof callbackCancelar === 'function') {
                callbackCancelar();
            }
            cerrarModalCancelar();
        });
    }

    const modal = document.getElementById('modal-cancelar');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                cerrarModalCancelar();
            }
        });
    }
});
