document.addEventListener('DOMContentLoaded', function () {
    $('#modalVerEvento').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);
        $('#verNombre').text(button.data('nombre') || '-');
        $('#verClienteEvento').text(button.data('cliente') || '-');
        $('#verTipo').text(button.data('tipo') || '-');
        $('#verEstadoEvento').text(button.data('estado') || '-');
        $('#verPresupuesto').text(button.data('presupuesto') || '0.00');
        $('#verDescripcionEvento').text(button.data('descripcion') || '-');
    });
});
