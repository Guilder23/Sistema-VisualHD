document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-eliminar-cita').forEach(function (button) {
        button.addEventListener('click', function () {
            document.getElementById('formEliminarCita').action = button.dataset.action;
            document.getElementById('eliminarCitaNombre').textContent = button.dataset.nombre || '';
        });
    });
});
