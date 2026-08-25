document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-ver-servicio').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.getElementById('ver_nombre').textContent = this.dataset.nombre || '-';
            document.getElementById('ver_descripcion').textContent = this.dataset.descripcion || '-';
            document.getElementById('ver_precio').textContent = this.dataset.precio || '-';
            document.getElementById('ver_duracion').textContent = `${this.dataset.duracion || '-'} min`;
            document.getElementById('ver_estado').textContent = this.dataset.estado || '-';
            document.getElementById('ver_creado').textContent = this.dataset.creado || '-';
        });
    });
});
