document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-eliminar-servicio').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEliminarServicio');
            form.action = this.dataset.action;
            document.getElementById('eliminarServicioNombre').textContent = this.dataset.nombre || '';
        });
    });
});
