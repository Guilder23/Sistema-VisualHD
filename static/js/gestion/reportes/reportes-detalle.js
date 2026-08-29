document.addEventListener('DOMContentLoaded', function () {
    const contenedor = document.querySelector('.reporte-detalle');
    if (!contenedor) return;

    const form = contenedor.querySelector('.reporte-filtros-form');
    const tabla = contenedor.querySelector('.tabla-reporte');
    const btnPdf = contenedor.querySelector('.btn-pdf-reporte');
    const resumenValor = contenedor.querySelector('[data-resumen-valor]');
    const resumenRegistros = contenedor.querySelector('[data-resumen-registros]');
    const esFinanciero = contenedor.dataset.tipo === 'financiero';

    function obtenerValoresFiltro() {
        if (!form) return {};
        const datos = {};
        form.querySelectorAll('input, select').forEach(function (el) {
            if (el.name) datos[el.name] = el.value;
        });
        return datos;
    }

    function filaVisible(fila, filtros) {
        const busqueda = (filtros.q || '').toLowerCase();
        if (busqueda && !(fila.dataset.search || '').includes(busqueda)) return false;
        if (filtros.estado && fila.dataset.estado !== filtros.estado) return false;
        if (filtros.categoria && fila.dataset.categoria !== filtros.categoria) return false;
        if (filtros.cargo && fila.dataset.cargo !== filtros.cargo) return false;

        const fecha = fila.dataset.fecha || '';
        if (filtros.fecha_inicio && fecha && fecha < filtros.fecha_inicio) return false;
        if (filtros.fecha_fin && fecha && fecha > filtros.fecha_fin) return false;

        return true;
    }

    function aplicarFiltros() {
        const filtros = obtenerValoresFiltro();

        if (esFinanciero) {
            return;
        }

        if (!tabla) return;
        let visibles = 0;
        let totalMonto = 0;

        tabla.querySelectorAll('tbody tr[data-search]').forEach(function (fila) {
            const visible = filaVisible(fila, filtros);
            fila.classList.toggle('filtro-oculto', !visible);
            if (visible) {
                visibles++;
                totalMonto += parseFloat(fila.dataset.monto || '0') || 0;
            }
        });

        if (resumenRegistros) resumenRegistros.textContent = visibles;
        if (resumenValor && contenedor.dataset.tieneMonto === 'true') {
            resumenValor.textContent = 'Bs. ' + totalMonto.toFixed(2);
        }
    }

    if (form) {
        form.querySelectorAll('input, select').forEach(function (el) {
            el.addEventListener('input', aplicarFiltros);
            el.addEventListener('change', function () {
                aplicarFiltros();
                if (esFinanciero) {
                    const params = new URLSearchParams(obtenerValoresFiltro());
                    window.location.href = window.location.pathname + '?' + params.toString();
                }
            });
        });
    }

    if (btnPdf && form) {
        btnPdf.addEventListener('click', function (e) {
            e.preventDefault();
            const baseUrl = form.dataset.pdfUrl;
            const params = new URLSearchParams(obtenerValoresFiltro());
            window.open(baseUrl + '?' + params.toString(), '_blank');
        });
    }

    aplicarFiltros();
});
