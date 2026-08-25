document.addEventListener('DOMContentLoaded', function () {
    const fecha = document.querySelector('#modalCrearCita input[name="fecha"]');
    if (fecha && !fecha.value) fecha.value = new Date().toISOString().slice(0, 16);
});
