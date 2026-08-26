document.addEventListener('DOMContentLoaded', function () {
    $('#modalEditarEvento').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);
        const form = $('#formEditarEvento');

        form.attr('action', button.data('action'));
        form.find('#editar_evento_cliente').val(button.data('clienteId') || '');
        form.find('#editar_evento_nombre').val(button.data('nombre') || '');
        form.find('#editar_evento_tipo').val(button.data('tipo') || '');
        form.find('#editar_evento_fecha_inicio').val(button.data('fechaInicio') || '');
        form.find('#editar_evento_fecha_fin').val(button.data('fechaFin') || '');
        form.find('#editar_evento_ubicacion').val(button.data('ubicacion') || '');
        form.find('#editar_evento_presupuesto').val(button.data('presupuesto') || '0');
        form.find('#editar_evento_estado').val(button.data('estado') || 'planificado');
        form.find('#editar_evento_descripcion').val(button.data('descripcion') || '');
    });
});
