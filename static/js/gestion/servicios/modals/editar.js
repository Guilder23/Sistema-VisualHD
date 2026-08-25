document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-editar-servicio').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEditarServicio');
            form.action = this.dataset.action;
            form.querySelector('#editar_nombre').value = this.dataset.nombre || '';
            form.querySelector('#editar_descripcion').value = this.dataset.descripcion || '';
            form.querySelector('#editar_precio').value = this.dataset.precio || '';
            form.querySelector('#editar_duracion_minutos').value = this.dataset.duracion || '';
            form.querySelector('#editar_estado').value = this.dataset.estado || 'activo';
        });
    });
});
