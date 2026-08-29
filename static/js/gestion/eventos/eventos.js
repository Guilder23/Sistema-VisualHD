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
    function mostrarDetallesPaquete(paqueteId, detallesDivId, nombreSpanId, detallesBodyId, precioTotalSpanId, onTotal) {
        const detallesDiv = document.getElementById(detallesDivId);
        if (!detallesDiv) return;

        if (!paqueteId) {
            detallesDiv.style.display = 'none';
            if (onTotal) onTotal(0);
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
                    if (onTotal) onTotal(Number(data.precio_total || 0));
                } else {
                    detallesDiv.style.display = 'none';
                    if (onTotal) onTotal(0);
                }
            })
            .catch(() => {
                detallesDiv.style.display = 'none';
                if (onTotal) onTotal(0);
            });
    }

    // ------------------- ADICIONALES (crear/editar) -------------------
    // Gestiona una lista editable de items adicionales y el total combinado (paquete + adicionales)
    function crearGestorAdicionales(prefix) {
        let items = [];
        let totalPaquete = 0;

        const cuerpo = document.getElementById(`${prefix}_adicionales_body`);
        const totalPaqueteSpan = document.getElementById(`${prefix}_total_paquete`);
        const totalAdicionalesSpan = document.getElementById(`${prefix}_total_adicionales`);
        const totalGeneralSpan = document.getElementById(`${prefix}_total_general`);
        const jsonInput = document.getElementById(`${prefix}_adicionales_json`);

        function render() {
            if (!cuerpo) return;
            cuerpo.innerHTML = '';
            let totalAdicionales = 0;

            items.forEach((item, index) => {
                const subtotal = item.precio_unitario * item.cantidad;
                totalAdicionales += subtotal;

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td><input type="text" class="form-control form-control-sm input-desc" data-index="${index}" value="${item.descripcion}"></td>
                    <td><input type="number" class="form-control form-control-sm input-precio" data-index="${index}" value="${item.precio_unitario}" step="0.01" min="0"></td>
                    <td><input type="number" class="form-control form-control-sm input-cant" data-index="${index}" value="${item.cantidad}" min="1"></td>
                    <td>Bs. ${subtotal.toFixed(2)}</td>
                    <td><button type="button" class="btn btn-danger btn-sm btn-quitar" data-index="${index}"><i class="fas fa-trash"></i></button></td>
                `;
                cuerpo.appendChild(row);
            });

            if (totalAdicionalesSpan) totalAdicionalesSpan.textContent = totalAdicionales.toFixed(2);
            if (totalPaqueteSpan) totalPaqueteSpan.textContent = totalPaquete.toFixed(2);
            if (totalGeneralSpan) totalGeneralSpan.textContent = (totalPaquete + totalAdicionales).toFixed(2);
            if (jsonInput) jsonInput.value = JSON.stringify(items);

            cuerpo.querySelectorAll('.input-desc').forEach(input => {
                input.addEventListener('change', function () {
                    items[this.dataset.index].descripcion = this.value;
                    if (jsonInput) jsonInput.value = JSON.stringify(items);
                });
            });
            cuerpo.querySelectorAll('.input-precio').forEach(input => {
                input.addEventListener('change', function () {
                    items[this.dataset.index].precio_unitario = parseFloat(this.value) || 0;
                    render();
                });
            });
            cuerpo.querySelectorAll('.input-cant').forEach(input => {
                input.addEventListener('change', function () {
                    items[this.dataset.index].cantidad = parseInt(this.value) || 1;
                    render();
                });
            });
            cuerpo.querySelectorAll('.btn-quitar').forEach(btn => {
                btn.addEventListener('click', function () {
                    items.splice(this.dataset.index, 1);
                    render();
                });
            });
        }

        return {
            agregar(descripcion, precioUnitario, cantidad) {
                items.push({ descripcion, precio_unitario: precioUnitario, cantidad });
                render();
            },
            setItems(nuevos) {
                items = nuevos || [];
                render();
            },
            setTotalPaquete(total) {
                totalPaquete = Number(total) || 0;
                render();
            },
            reset() {
                items = [];
                totalPaquete = 0;
                render();
            }
        };
    }

    // Enlaza el formulario de agregar item adicional (descripcion/precio/cantidad/botón) con un gestor
    function enlazarFormularioAdicional(prefix, gestor) {
        const btn = document.getElementById(`${prefix}_btn_agregar_adicional`);
        const descInput = document.getElementById(`${prefix}_adicional_descripcion`);
        const precioInput = document.getElementById(`${prefix}_adicional_precio`);
        const cantInput = document.getElementById(`${prefix}_adicional_cantidad`);
        if (!btn) return;

        btn.addEventListener('click', function () {
            const descripcion = (descInput.value || '').trim();
            if (!descripcion) {
                alert('Ingrese una descripción para el adicional');
                return;
            }
            const precio = parseFloat(precioInput.value) || 0;
            const cantidad = parseInt(cantInput.value) || 1;
            gestor.agregar(descripcion, precio, cantidad);
            descInput.value = '';
            precioInput.value = '';
            cantInput.value = 1;
        });
    }

    const gestorAdicionalesCrear = crearGestorAdicionales('crear_evento');
    enlazarFormularioAdicional('crear_evento', gestorAdicionalesCrear);
    window.gestorAdicionalesCrear = gestorAdicionalesCrear;

    const gestorAdicionalesEditar = crearGestorAdicionales('editar_evento');
    enlazarFormularioAdicional('editar_evento', gestorAdicionalesEditar);
    window.gestorAdicionalesEditar = gestorAdicionalesEditar;

    const modalCrearEvento = document.getElementById('modalCrearEvento');
    if (modalCrearEvento) {
        modalCrearEvento.addEventListener('hidden.bs.modal', function () {
            gestorAdicionalesCrear.reset();
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
                gestorAdicionalesCrear.setTotalPaquete(0);
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
                'crear_paquete_precio_total',
                function (total) { gestorAdicionalesCrear.setTotalPaquete(total); }
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
                gestorAdicionalesEditar.setTotalPaquete(0);
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
                'editar_paquete_precio_total',
                function (total) { gestorAdicionalesEditar.setTotalPaquete(total); }
            );
        });
    }

    // Función que llama el modal editar para inicializar el select al abrirlo
    window.cargarPaquetesEditar = function(servicioId, paqueteId, adicionales) {
        gestorAdicionalesEditar.setItems(adicionales || []);
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
                        'editar_paquete_precio_total',
                        function (total) { gestorAdicionalesEditar.setTotalPaquete(total); }
                    );
                } else {
                    gestorAdicionalesEditar.setTotalPaquete(0);
                }
            });
        } else {
            if (editarPaqueteSelect) {
                editarPaqueteSelect.innerHTML = '<option value="">Seleccione un servicio primero...</option>';
                editarPaqueteSelect.disabled = true;
            }
            gestorAdicionalesEditar.setTotalPaquete(0);
        }
    };

    // Función que llama el modal ver
    window.mostrarPaqueteVer = function(paqueteId, paqueteNombre) {
        const verPaquete = document.getElementById('verPaquete');
        const verDetalles = document.getElementById('verPaqueteDetalles');
        const totalPaqueteSpan = document.getElementById('verTotalPaquete');
        const totalGeneralSpan = document.getElementById('verTotalGeneral');

        function actualizarTotalGeneral(totalPaquete) {
            const totalAdicionales = parseFloat((document.getElementById('verTotalAdicionales') || {}).textContent) || 0;
            if (totalPaqueteSpan) totalPaqueteSpan.textContent = totalPaquete.toFixed(2);
            if (totalGeneralSpan) totalGeneralSpan.textContent = (totalPaquete + totalAdicionales).toFixed(2);
        }

        if (paqueteId) {
            if (verPaquete) verPaquete.textContent = paqueteNombre;
            mostrarDetallesPaquete(
                paqueteId,
                'verPaqueteDetalles',
                'verPaqueteNombre',
                'verPaqueteDetallesBody',
                'verPaquetePrecioTotal',
                actualizarTotalGeneral
            );
        } else {
            if (verPaquete) verPaquete.textContent = 'No asignado';
            if (verDetalles) verDetalles.style.display = 'none';
            actualizarTotalGeneral(0);
        }
    };

    // Función que llama el modal ver para mostrar los adicionales del evento (solo lectura)
    window.mostrarAdicionalesVer = function(adicionalesStr) {
        const contenedor = document.getElementById('verAdicionalesDetalles');
        const cuerpo = document.getElementById('verAdicionalesDetallesBody');
        const totalAdicionalesSpan = document.getElementById('verTotalAdicionales');
        const totalPaqueteSpan = document.getElementById('verTotalPaquete');
        const totalGeneralSpan = document.getElementById('verTotalGeneral');
        if (!cuerpo) return;

        cuerpo.innerHTML = '';
        let totalAdicionales = 0;

        if (adicionalesStr) {
            adicionalesStr.split(';').forEach(function (item) {
                const parts = item.split('|');
                if (parts.length === 3) {
                    const descripcion = parts[0];
                    const precioUnitario = parseFloat((parts[1] || '0').replace(',', '.')) || 0;
                    const cantidad = parseInt(parts[2]) || 1;
                    const subtotal = precioUnitario * cantidad;
                    totalAdicionales += subtotal;

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${descripcion}</td>
                        <td>Bs. ${precioUnitario.toFixed(2)}</td>
                        <td>${cantidad}</td>
                        <td>Bs. ${subtotal.toFixed(2)}</td>
                    `;
                    cuerpo.appendChild(row);
                }
            });
        }

        if (contenedor) contenedor.style.display = totalAdicionales > 0 || cuerpo.children.length > 0 ? 'block' : 'none';
        if (totalAdicionalesSpan) totalAdicionalesSpan.textContent = totalAdicionales.toFixed(2);

        const totalPaquete = parseFloat(totalPaqueteSpan ? totalPaqueteSpan.textContent : '0') || 0;
        if (totalGeneralSpan) totalGeneralSpan.textContent = (totalPaquete + totalAdicionales).toFixed(2);
    };
});
