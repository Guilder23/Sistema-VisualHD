document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-eliminar-evento').forEach(function (button) {
        button.addEventListener('click', function () {
            document.getElementById('formEliminarEvento').action = button.dataset.action;
            document.getElementById('eliminarEventoNombre').textContent = button.dataset.nombre || '';
        });
    });
});
