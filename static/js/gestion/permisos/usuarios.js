document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.usuarios-card tbody tr').forEach(function (fila) {
        fila.addEventListener('mouseenter', function () {
            fila.classList.add('fila-activa');
        });
        fila.addEventListener('mouseleave', function () {
            fila.classList.remove('fila-activa');
        });
    });
});
