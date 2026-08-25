document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-eliminar-sesion').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEliminarSesion');
            form.action = this.dataset.action;
            document.getElementById('eliminarSesionNombre').textContent = this.dataset.nombre || '';
        });
    });
});
