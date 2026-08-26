document.addEventListener('DOMContentLoaded', function () {
    const filtroSelect = document.querySelector('.card-filtros select[name="tipo"]');
    if (filtroSelect) {
        filtroSelect.addEventListener('change', function () {
            this.form.submit();
        });
    }

    // Modal Amortizar
    document.querySelectorAll('.btn-amortizar').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.querySelector('#formAmortizar');
            document.getElementById('amortizar_tipo').value = this.dataset.tipo;
            document.getElementById('amortizar_objeto_id').value = this.dataset.id;
            document.getElementById('amortizar-nombre').textContent = this.dataset.nombre;
            document.getElementById('amortizar-total').textContent = 'Bs. ' + this.dataset.total;
            document.getElementById('amortizar-pagado').textContent = 'Bs. ' + this.dataset.pagado;
            document.getElementById('amortizar-pendiente').textContent = 'Bs. ' + this.dataset.pendiente;
            form.querySelector('[name="monto_amortizar"]').value = '';
            form.querySelector('[name="monto_amortizar"]').max = this.dataset.pendiente;
            form.querySelector('[name="fecha_amortizacion"]').value = new Date().toISOString().split('T')[0];
        });
    });
});
