let callbackConfirmar = null;

function abrirModalConfirmar(titulo, mensaje, callback) {
    document.getElementById('modal-confirmar-titulo').textContent = titulo || 'Confirmar acción';
    document.getElementById('modal-confirmar-mensaje').textContent = mensaje || '¿Estás seguro de que quieres continuar?';
    callbackConfirmar = callback;
    document.getElementById('modal-confirmar').showModal();
}

function cerrarModalConfirmar() {
    document.getElementById('modal-confirmar').close();
    callbackConfirmar = null;
}

document.addEventListener('DOMContentLoaded', function() {
    const confirmarBtn = document.getElementById('modal-confirmar-btn');
    if (confirmarBtn) {
        confirmarBtn.addEventListener('click', async function() {
            if (callbackConfirmar && typeof callbackConfirmar === 'function') {
                const result = callbackConfirmar();
                if (result && typeof result.then === 'function') {
                    await result;
                }
            }
            cerrarModalConfirmar();
        });
    }

    const modal = document.getElementById('modal-confirmar');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                cerrarModalConfirmar();
            }
        });
    }
});
