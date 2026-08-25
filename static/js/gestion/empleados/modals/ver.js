document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-ver-empleado').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.getElementById('ver_nombre_completo').textContent = `${this.dataset.nombre || ''} ${this.dataset.apellido || ''}`.trim();
            document.getElementById('ver_cargo').textContent = this.dataset.cargo || '-';
            document.getElementById('ver_telefono').textContent = this.dataset.telefono || '-';
            document.getElementById('ver_email').textContent = this.dataset.email || '-';
            document.getElementById('ver_estado').textContent = this.dataset.estado || '-';
            document.getElementById('ver_observacion').textContent = this.dataset.observacion || '-';
            document.getElementById('ver_ingreso').textContent = this.dataset.ingreso || '-';
        });
    });
});
