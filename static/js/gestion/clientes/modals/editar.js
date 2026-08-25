document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-editar-cliente').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEditarCliente');
            form.action = this.dataset.action;
            form.querySelector('#editar_nombre').value = this.dataset.nombre || '';
            form.querySelector('#editar_apellido').value = this.dataset.apellido || '';
            form.querySelector('#editar_email').value = this.dataset.email || '';
            form.querySelector('#editar_telefono').value = this.dataset.telefono || '';
            form.querySelector('#editar_ci').value = this.dataset.ci || '';
            form.querySelector('#editar_ciudad').value = this.dataset.ciudad || '';
            form.querySelector('#editar_direccion').value = this.dataset.direccion || '';
            form.querySelector('#editar_fecha_nacimiento').value = this.dataset.fechaNacimiento || '';
            form.querySelector('#editar_estado').value = this.dataset.estado || 'activo';
            form.querySelector('#editar_observacion').value = this.dataset.observacion || '';
        });
    });
});
