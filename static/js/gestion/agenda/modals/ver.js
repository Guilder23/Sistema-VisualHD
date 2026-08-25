document.addEventListener('DOMContentLoaded', function () {
    $('#modalVerCita').on('show.bs.modal', function (event) {
        const button = $(event.relatedTarget);
        $('#verCliente').text(button.data('cliente') || '-');
        $('#verFecha').text(button.data('fecha') || '-');
        $('#verEmpleado').text(button.data('empleado') || '-');
        $('#verDuracion').text(button.data('duracion') || '-');
        $('#verDescripcion').text(button.data('descripcion') || '-');
        $('#verUbicacion').text(button.data('ubicacion') || '-');
        $('#verEstado').text(button.data('estado') || '-');
    });
});
