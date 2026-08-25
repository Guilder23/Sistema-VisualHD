document.addEventListener('DOMContentLoaded', function () {
    const filtroSelect = document.querySelector('.card-filtros select[name="estado"]');
    if (filtroSelect) {
        filtroSelect.addEventListener('change', function () {
            this.form.submit();
        });
    }
});
