document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-eliminar-cliente').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEliminarCliente');
            form.action = this.dataset.action;
            document.getElementById('eliminarClienteNombre').textContent = this.dataset.nombre || '';
        });
    });
});
