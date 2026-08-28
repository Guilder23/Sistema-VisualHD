document.addEventListener('DOMContentLoaded', function () {
    $('#modalEditarEvento').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);
        const form = $('#formEditarEvento');

        form.attr('action', button.data('action'));
        form.find('#editar_evento_cliente').val(button.data('clienteId') || '');
        form.find('#editar_evento_nombre').val(button.data('nombre') || '');
        form.find('#editar_evento_fecha_inicio').val(button.data('fechaInicio') || '');
        form.find('#editar_evento_fecha_fin').val(button.data('fechaFin') || '');
        form.find('#editar_evento_ubicacion').val(button.data('ubicacion') || '');
        form.find('#editar_evento_estado').val(button.data('estado') || 'planificado');
        form.find('#editar_evento_descripcion').val(button.data('descripcion') || '');
        
        const servicioId = button.data('servicioId');
        const paqueteId = button.data('paqueteId');
        const adicionalesStr = button.data('adicionales') || '';

        const adicionales = [];
        adicionalesStr.split(';').forEach(function (item) {
            const parts = String(item).split('|');
            if (parts.length === 3) {
                adicionales.push({
                    descripcion: parts[0],
                    precio_unitario: parseFloat((parts[1] || '0').replace(',', '.')) || 0,
                    cantidad: parseInt(parts[2]) || 1
                });
            }
        });
        
        if (typeof cargarPaquetesEditar === 'function') {
            cargarPaquetesEditar(servicioId, paqueteId, adicionales);
        }
    });
});
