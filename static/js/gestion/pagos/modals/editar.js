document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-editar-pago').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEditarPago');
            form.action = this.dataset.action;
            form.querySelector('#editar_cliente_id').value = this.dataset.clienteId || '';
            form.querySelector('#editar_sesion_id').value = this.dataset.sesionId || '';
            form.querySelector('#editar_evento_id').value = this.dataset.eventoId || '';
            form.querySelector('#editar_monto').value = this.dataset.monto || '';
            form.querySelector('#editar_monto_pagado').value = this.dataset.montoPagado || '';
            form.querySelector('#editar_metodo_pago').value = this.dataset.metodo || 'efectivo';
            form.querySelector('#editar_estado').value = this.dataset.estado || 'pendiente';
            form.querySelector('#editar_fecha_pago').value = this.dataset.fecha || '';
            form.querySelector('#editar_observacion').value = this.dataset.observacion || '';
        });
    });

    // Auto-fill monto when selecting sesion or evento
    const sesionSelect = document.getElementById('editar_sesion_id');
    const eventoSelect = document.getElementById('editar_evento_id');
    const montoInput = document.getElementById('editar_monto');

    sesionSelect.addEventListener('change', function () {
        if (this.value) {
            const selectedOption = this.options[this.selectedIndex];
            const precio = selectedOption.dataset.precio;
            if (precio) {
                montoInput.value = precio;
            }
        }
    });

    eventoSelect.addEventListener('change', function () {
        if (this.value) {
            const selectedOption = this.options[this.selectedIndex];
            const precio = selectedOption.dataset.precio;
            if (precio) {
                montoInput.value = precio;
            }
        }
    });
});
