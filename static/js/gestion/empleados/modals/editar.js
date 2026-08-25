document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-editar-empleado').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEditarEmpleado');
            form.action = this.dataset.action;
            form.querySelector('#editar_nombre').value = this.dataset.nombre || '';
            form.querySelector('#editar_apellido').value = this.dataset.apellido || '';
            form.querySelector('#editar_cargo').value = this.dataset.cargo || 'fotografo';
            form.querySelector('#editar_telefono').value = this.dataset.telefono || '';
            form.querySelector('#editar_email').value = this.dataset.email || '';
            form.querySelector('#editar_estado').value = this.dataset.estado || 'activo';
            form.querySelector('#editar_observacion').value = this.dataset.observacion || '';
        });
    });
});
