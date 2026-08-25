document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalEditarEgreso');
    if (!modal) return;

    modal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const form = document.getElementById('formEditarEgreso');
        form.action = button.dataset.action;
        document.getElementById('editarCategoria').value = button.dataset.categoria || 'otro';
        document.getElementById('editarFecha').value = button.dataset.fecha || '';
        document.getElementById('editarConcepto').value = button.dataset.concepto || '';
        document.getElementById('editarMonto').value = button.dataset.monto || '';
        document.getElementById('editarComprobante').value = button.dataset.comprobante || '';
        document.getElementById('editarNotas').value = button.dataset.notas || '';
    });
});
