document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-ver-pago').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.getElementById('ver_cliente').textContent = this.dataset.cliente || '-';
            document.getElementById('ver_sesion').textContent = this.dataset.sesion || '-';
            document.getElementById('ver_monto').textContent = this.dataset.monto || '-';
            document.getElementById('ver_metodo').textContent = this.dataset.metodo || '-';
            document.getElementById('ver_estado').textContent = this.dataset.estado || '-';
            document.getElementById('ver_fecha').textContent = this.dataset.fecha || '-';
            document.getElementById('ver_observacion').textContent = this.dataset.observacion || '-';
        });
    });
});
