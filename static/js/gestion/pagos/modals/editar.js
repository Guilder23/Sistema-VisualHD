document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-editar-pago').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEditarPago');
            form.action = this.dataset.action;
            form.querySelector('#editar_cliente_id').value = this.dataset.clienteId || '';
            form.querySelector('#editar_sesion_id').value = this.dataset.sesionId || '';
            form.querySelector('#editar_monto').value = this.dataset.monto || '';
            form.querySelector('#editar_metodo_pago').value = this.dataset.metodo || 'efectivo';
            form.querySelector('#editar_estado').value = this.dataset.estado || 'pendiente';
            form.querySelector('#editar_fecha_pago').value = this.dataset.fecha || '';
            form.querySelector('#editar_observacion').value = this.dataset.observacion || '';
        });
    });
});
