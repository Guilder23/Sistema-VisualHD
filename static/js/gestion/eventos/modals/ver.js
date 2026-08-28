document.addEventListener('DOMContentLoaded', function () {
    $('#modalVerEvento').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);
        $('#verNombre').text(button.data('nombre') || '-');
        $('#verClienteEvento').text(button.data('cliente') || '-');
        $('#verServicio').text(button.data('servicio') || '-');
        $('#verFechaInicio').text(button.data('fechaInicio') || '-');
        $('#verFechaFin').text(button.data('fechaFin') || '-');
        $('#verUbicacion').text(button.data('ubicacion') || '-');
        $('#verEstadoEvento').text(button.data('estado') || '-');
        $('#verPresupuesto').text(button.data('presupuesto') || '0.00');
        $('#verDescripcionEvento').text(button.data('descripcion') || '-');
        
        const paqueteId = button.data('paqueteId');
        const paqueteNombre = button.data('paqueteNombre');
        
        if (typeof mostrarPaqueteVer === 'function') {
            mostrarPaqueteVer(paqueteId, paqueteNombre);
        }
    });
});
