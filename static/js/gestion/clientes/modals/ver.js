document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-ver-cliente').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.getElementById('ver_nombre_completo').textContent = `${this.dataset.nombre || ''} ${this.dataset.apellido || ''}`.trim();
            document.getElementById('ver_email').textContent = this.dataset.email || '-';
            document.getElementById('ver_telefono').textContent = this.dataset.telefono || '-';
            document.getElementById('ver_ci').textContent = this.dataset.ci || '-';
            document.getElementById('ver_ciudad').textContent = this.dataset.ciudad || '-';
            document.getElementById('ver_direccion').textContent = this.dataset.direccion || '-';
            document.getElementById('ver_fecha_nacimiento').textContent = this.dataset.fechaNacimiento || '-';
            document.getElementById('ver_estado').textContent = this.dataset.estado || '-';
            document.getElementById('ver_observacion').textContent = this.dataset.observacion || '-';
            document.getElementById('ver_creado').textContent = this.dataset.creado || '-';
        });
    });
});
