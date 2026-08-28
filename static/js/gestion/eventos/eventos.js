// Eventos
document.addEventListener('DOMContentLoaded', function() {

    const PAQUETES = (typeof window.PAQUETES_GLOBALES !== 'undefined' && Array.isArray(window.PAQUETES_GLOBALES))
        ? window.PAQUETES_GLOBALES
        : [];

    // Poblar el select de paquetes con una lista (siempre habilita el select)
    function poblarPaquetes(paqueteSelect, paquetes) {
        paqueteSelect.innerHTML = '';
        if (paquetes && paquetes.length > 0) {
            const opDefault = document.createElement('option');
            opDefault.value = '';
            opDefault.textContent = 'Seleccionar paquete...';
            paqueteSelect.appendChild(opDefault);
            paquetes.forEach(paquete => {
                const option = document.createElement('option');
                option.value = paquete.id;
                const precio = Number(paquete.precio_total || 0).toFixed(2);
                option.textContent = `${paquete.nombre} - Bs. ${precio}`;
                paqueteSelect.appendChild(option);
            });
        } else {
            const opNone = document.createElement('option');
            opNone.value = '';
            opNone.textContent = 'No hay paquetes disponibles para este servicio';
            paqueteSelect.appendChild(opNone);
        }
        paqueteSelect.disabled = false;
    }

    // Cargar paquetes POR SERVICIO: PRIMERO usa la lista local embebida, luego intenta fetch como refuerzo
    function cargarPaquetesPorServicio(servicioId, paqueteSelectId, callback) {
        const paqueteSelect = document.getElementById(paqueteSelectId);
        if (!paqueteSelect) { if (callback) callback(); return; }

        if (!servicioId) {
            paqueteSelect.innerHTML = '<option value="">Seleccione un servicio primero...</option>';
            paqueteSelect.disabled = true;
            if (callback) callback();
            return;
        }

        // 1) Mostrar inmediatamente desde la fuente local embebida (funciona siempre)
        const locales = PAQUETES.filter(p => String(p.servicio_principal_id) === String(servicioId));
        poblarPaquetes(paqueteSelect, locales);

        // 2) Refrescar silenciosamente con la API si está disponible (no bloquea, no muestra error)
        fetch(`/gestion/eventos/api/paquetes-por-servicio/?servicio_id=${encodeURIComponent(servicioId)}`, {
            method: 'GET',
            credentials: 'same-origin',
            headers: { 'Accept': 'application/json' }
        })
            .then(response => {
                if (!response.ok) throw new Error('HTTP ' + response.status);
                return response.json();
            })
            .then(data => {
                if (data && Array.isArray(data.paquetes) && data.paquetes.length >= 0) {
                    poblarPaquetes(paqueteSelect, data.paquetes);
                }
            })
            .catch(() => {
                // Silencioso: si la API falla, la fuente local ya fue mostrada
            });

        if (callback) callback();
    }

    // Mostrar detalles del paquete seleccionado (contenido, precios, subtotal, total)
    function mostrarDetallesPaquete(paqueteId, detallesDivId, nombreSpanId, detallesBodyId, precioTotalSpanId) {
        const detallesDiv = document.getElementById(detallesDivId);
        if (!detallesDiv) return;

        if (!paqueteId) {
            detallesDiv.style.display = 'none';
            return;
        }

        fetch(`/gestion/eventos/api/detalle-paquete/?paquete_id=${encodeURIComponent(paqueteId)}`, {
            method: 'GET',
            credentials: 'same-origin',
            headers: { 'Accept': 'application/json' }
        })
            .then(response => {
                if (!response.ok) throw new Error('HTTP ' + response.status);
                return response.json();
            })
            .then(data => {
                const nombreSpan = document.getElementById(nombreSpanId);
                const detallesBody = document.getElementById(detallesBodyId);
                const precioTotalSpan = document.getElementById(precioTotalSpanId);

                if (data.detalles && data.detalles.length > 0) {
                    if (nombreSpan) nombreSpan.textContent = data.nombre;
                    if (detallesBody) {
                        detallesBody.innerHTML = '';
                        data.detalles.forEach(detalle => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${detalle.descripcion}</td>
                                <td>Bs. ${Number(detalle.precio_unitario || 0).toFixed(2)}</td>
                                <td>${detalle.cantidad}</td>
                                <td>Bs. ${Number(detalle.subtotal || 0).toFixed(2)}</td>
                            `;
                            detallesBody.appendChild(row);
                        });
                    }
                    if (precioTotalSpan) precioTotalSpan.textContent = Number(data.precio_total || 0).toFixed(2);
                    detallesDiv.style.display = 'block';
                } else {
                    detallesDiv.style.display = 'none';
                }
            })
            .catch(() => {
                detallesDiv.style.display = 'none';
            });
    }

    // ------------------- MODAL CREAR -------------------
    const crearServicioSelect = document.getElementById('crear_evento_servicio');
    const crearPaqueteSelect = document.getElementById('crear_evento_paquete');

    if (crearServicioSelect) {
        crearServicioSelect.addEventListener('change', function() {
            const servicioId = this.value;
            cargarPaquetesPorServicio(servicioId, 'crear_evento_paquete', function() {
                const detalles = document.getElementById('crear_paquete_detalles');
                if (detalles) detalles.style.display = 'none';
            });
        });
    }

    if (crearPaqueteSelect) {
        crearPaqueteSelect.addEventListener('change', function() {
            const paqueteId = this.value;
            mostrarDetallesPaquete(
                paqueteId,
                'crear_paquete_detalles',
                'crear_paquete_nombre',
                'crear_paquete_detalles_body',
                'crear_paquete_precio_total'
            );
        });
    }

    // ------------------- MODAL EDITAR -------------------
    const editarServicioSelect = document.getElementById('editar_evento_servicio');
    const editarPaqueteSelect = document.getElementById('editar_evento_paquete');

    if (editarServicioSelect) {
        editarServicioSelect.addEventListener('change', function() {
            const servicioId = this.value;
            cargarPaquetesPorServicio(servicioId, 'editar_evento_paquete', function() {
                const detalles = document.getElementById('editar_paquete_detalles');
                if (detalles) detalles.style.display = 'none';
            });
        });
    }

    if (editarPaqueteSelect) {
        editarPaqueteSelect.addEventListener('change', function() {
            const paqueteId = this.value;
            mostrarDetallesPaquete(
                paqueteId,
                'editar_paquete_detalles',
                'editar_paquete_nombre',
                'editar_paquete_detalles_body',
                'editar_paquete_precio_total'
            );
        });
    }

    // Función que llama el modal editar para inicializar el select al abrirlo
    window.cargarPaquetesEditar = function(servicioId, paqueteId) {
        if (servicioId && editarServicioSelect) {
            editarServicioSelect.value = servicioId;
            cargarPaquetesPorServicio(servicioId, 'editar_evento_paquete', function() {
                if (paqueteId && editarPaqueteSelect) {
                    editarPaqueteSelect.value = paqueteId;
                    mostrarDetallesPaquete(
                        paqueteId,
                        'editar_paquete_detalles',
                        'editar_paquete_nombre',
                        'editar_paquete_detalles_body',
                        'editar_paquete_precio_total'
                    );
                }
            });
        } else {
            if (editarPaqueteSelect) {
                editarPaqueteSelect.innerHTML = '<option value="">Seleccione un servicio primero...</option>';
                editarPaqueteSelect.disabled = true;
            }
        }
    };

    // Función que llama el modal ver
    window.mostrarPaqueteVer = function(paqueteId, paqueteNombre) {
        const verPaquete = document.getElementById('verPaquete');
        const verDetalles = document.getElementById('verPaqueteDetalles');

        if (paqueteId) {
            if (verPaquete) verPaquete.textContent = paqueteNombre;
            mostrarDetallesPaquete(
                paqueteId,
                'verPaqueteDetalles',
                'verPaqueteNombre',
                'verPaqueteDetallesBody',
                'verPaquetePrecioTotal'
            );
        } else {
            if (verPaquete) verPaquete.textContent = 'No asignado';
            if (verDetalles) verDetalles.style.display = 'none';
        }
    };
});
