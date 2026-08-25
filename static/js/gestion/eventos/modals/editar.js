document.addEventListener('DOMContentLoaded', function () {
    $('#modalEditarEvento').on('show.bs.modal', function (event) {
        $('#formEditarEvento').attr('action', $(event.relatedTarget).data('action'));
    });
});
