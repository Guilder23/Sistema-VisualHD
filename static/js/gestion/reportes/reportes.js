document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-reporte]').forEach(function (elemento) {
        elemento.addEventListener('click', function () {
            document.querySelectorAll('[data-reporte]').forEach(function (item) {
                item.classList.remove('active');
            });
            elemento.classList.add('active');
        });
    });
});
