document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-eliminar-pago').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEliminarPago');
            form.action = this.dataset.action;
            document.getElementById('eliminarPagoNombre').textContent = this.dataset.nombre || '';
        });
    });
});
