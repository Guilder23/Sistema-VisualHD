document.addEventListener('DOMContentLoaded', function () {
    // Modal Ver Pago
    document.querySelectorAll('.btn-ver-pago').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.getElementById('ver-empleado').textContent = this.dataset.empleado;
            document.getElementById('ver-mes-año').textContent = this.dataset.mesAño;
            document.getElementById('ver-monto-base').textContent = 'Bs. ' + this.dataset.montoBase;
            document.getElementById('ver-bonificacion').textContent = 'Bs. ' + this.dataset.bonificacion;
            document.getElementById('ver-descuentos').textContent = 'Bs. ' + this.dataset.descuentos;
            document.getElementById('ver-total').textContent = 'Bs. ' + this.dataset.total;
            document.getElementById('ver-pagado').textContent = 'Bs. ' + this.dataset.pagado;
            document.getElementById('ver-estado').textContent = this.dataset.estado;
            document.getElementById('ver-fecha').textContent = this.dataset.fecha;
            document.getElementById('ver-comprobante').textContent = this.dataset.comprobante || '-';
            document.getElementById('ver-notas').textContent = this.dataset.notas || '-';
        });
    });

    // Modal Editar Pago
    document.querySelectorAll('.btn-editar-pago').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.querySelector('#formEditarPagoEmpleado');
            form.action = this.dataset.action;
            form.querySelector('[name="empleado_id"]').value = this.dataset.empleadoId;
            form.querySelector('[name="mes_año"]').value = this.dataset.mesAño;
            form.querySelector('[name="monto_base"]').value = this.dataset.montoBase;
            form.querySelector('[name="bonificacion"]').value = this.dataset.bonificacion;
            form.querySelector('[name="descuentos"]').value = this.dataset.descuentos;
            form.querySelector('[name="total_a_pagar"]').value = this.dataset.total;
            form.querySelector('[name="monto_pagado"]').value = this.dataset.pagado;
            form.querySelector('[name="estado"]').value = this.dataset.estado;
            form.querySelector('[name="fecha_pago"]').value = this.dataset.fecha;
            form.querySelector('[name="comprobante"]').value = this.dataset.comprobante;
            form.querySelector('[name="notas"]').value = this.dataset.notas;
        });
    });

    // Modal Anular Pago
    document.querySelectorAll('.btn-anular-pago').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.querySelector('#formAnularPagoEmpleado');
            form.action = this.dataset.action;
            document.getElementById('anular-nombre').textContent = this.dataset.nombre;
        });
    });

    // Modal Amortizar Pago
    document.querySelectorAll('.btn-amortizar-pago').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.querySelector('#formAmortizarPagoEmpleado');
            form.action = this.dataset.action;
            document.getElementById('amortizar-nombre').textContent = this.dataset.nombre;
            document.getElementById('amortizar-total').textContent = 'Bs. ' + this.dataset.total;
            document.getElementById('amortizar-pagado').textContent = 'Bs. ' + this.dataset.pagado;
            const pendiente = (parseFloat(this.dataset.total) - parseFloat(this.dataset.pagado)).toFixed(2);
            document.getElementById('amortizar-pendiente').textContent = 'Bs. ' + pendiente;
            form.querySelector('[name="monto_amortizar"]').value = '';
            form.querySelector('[name="monto_amortizar"]').max = pendiente;
            form.querySelector('[name="fecha_amortizacion"]').value = new Date().toISOString().split('T')[0];
        });
    });
});
