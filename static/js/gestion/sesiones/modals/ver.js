document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-ver-sesion').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.getElementById('ver_cliente').textContent = this.dataset.cliente || '-';
            document.getElementById('ver_servicio').textContent = this.dataset.servicio || '-';
            document.getElementById('ver_empleado').textContent = this.dataset.empleado || '-';
            document.getElementById('ver_fecha').textContent = this.dataset.fecha || '-';
            document.getElementById('ver_hora').textContent = this.dataset.hora || '-';
            document.getElementById('ver_lugar').textContent = this.dataset.lugar || '-';
            document.getElementById('ver_precio').textContent = 'Bs. ' + (this.dataset.precio || '0');
            document.getElementById('ver_estado').textContent = this.dataset.estado || '-';
            document.getElementById('ver_observacion').textContent = this.dataset.observacion || '-';
        });
    });
});
