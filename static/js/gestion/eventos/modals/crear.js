document.addEventListener('DOMContentLoaded', function () {
    const fechaInicio = document.querySelector('#modalCrearEvento input[name="fecha_inicio"]');
    if (fechaInicio && !fechaInicio.value) fechaInicio.value = new Date().toISOString().slice(0, 16);
});
