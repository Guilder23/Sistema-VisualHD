document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-eliminar-paquete').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEliminarPaquete');
            form.action = this.dataset.action;
            document.getElementById('eliminarPaqueteNombre').textContent = this.dataset.nombre || '';
        });
    });
});
