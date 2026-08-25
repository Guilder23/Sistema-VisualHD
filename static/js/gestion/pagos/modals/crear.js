document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalCrearPago');
    if (!modal) return;
    modal.addEventListener('hidden.bs.modal', function () {
        modal.querySelector('form').reset();
    });
});
