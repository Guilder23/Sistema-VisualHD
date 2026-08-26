document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalCrearPago');
    if (!modal) return;
    
    modal.addEventListener('hidden.bs.modal', function () {
        modal.querySelector('form').reset();
    });

    // Auto-fill monto when selecting sesion or evento
    const sesionSelect = document.getElementById('crear_sesion_id');
    const eventoSelect = document.getElementById('crear_evento_id');
    const montoInput = document.getElementById('crear_monto');

    sesionSelect.addEventListener('change', function () {
        if (this.value) {
            const selectedOption = this.options[this.selectedIndex];
            const precio = selectedOption.dataset.precio;
            if (precio) {
                montoInput.value = precio;
            }
        }
    });

    eventoSelect.addEventListener('change', function () {
        if (this.value) {
            const selectedOption = this.options[this.selectedIndex];
            const precio = selectedOption.dataset.precio;
            if (precio) {
                montoInput.value = precio;
            }
        }
    });
});
