document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-eliminar-empleado').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEliminarEmpleado');
            form.action = this.dataset.action;
            document.getElementById('eliminarEmpleadoNombre').textContent = this.dataset.nombre || '';
        });
    });
});
