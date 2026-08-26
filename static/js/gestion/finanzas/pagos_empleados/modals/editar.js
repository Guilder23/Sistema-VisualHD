document.addEventListener('DOMContentLoaded', function () {
    const formulario = document.querySelector('#formEditarPagoEmpleado');
    if (!formulario) return;

    const base = formulario.querySelector('[name="monto_base"]');
    const bonificacion = formulario.querySelector('[name="bonificacion"]');
    const descuentos = formulario.querySelector('[name="descuentos"]');
    const total = formulario.querySelector('[name="total_a_pagar"]');

    function calcularTotal() {
        const montoBase = parseFloat(base.value) || 0;
        const extra = parseFloat(bonificacion.value) || 0;
        const descuento = parseFloat(descuentos.value) || 0;
        total.value = Math.max(0, montoBase + extra - descuento).toFixed(2);
    }

    [base, bonificacion, descuentos].forEach(function (campo) {
        campo.addEventListener('input', calcularTotal);
    });
});
