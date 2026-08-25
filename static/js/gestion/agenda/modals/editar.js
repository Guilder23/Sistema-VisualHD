document.addEventListener('DOMContentLoaded', function () {
    $('#modalEditarCita').on('show.bs.modal', function (event) {
        $('#formEditarCita').attr('action', $(event.relatedTarget).data('action'));
    });
});
