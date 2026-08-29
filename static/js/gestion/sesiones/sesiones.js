document.addEventListener('DOMContentLoaded', function () {
    const filtroSelect = document.querySelector('.card-filtros select[name="estado"]');
    if (filtroSelect) {
        filtroSelect.addEventListener('change', function () {
            this.form.submit();
        });
    }

    function crearGestorAdicionales(prefix) {
        let items = [];

        const cuerpo = document.getElementById(`${prefix}_adicionales_body`);
        const totalSpan = document.getElementById(`${prefix}_total`);
        const jsonInput = document.getElementById(`${prefix}_adicionales_json`);

        function render() {
            if (!cuerpo) return;
            cuerpo.innerHTML = '';
            let total = 0;

            items.forEach((item, index) => {
                const subtotal = item.precio_unitario * item.cantidad;
                total += subtotal;

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

            if (totalSpan) totalSpan.textContent = total.toFixed(2);
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
            reset() {
                items = [];
                render();
            },
            render
        };
    }

    function enlazarFormularioAdicional(prefix, gestor) {
        const btn = document.getElementById(`${prefix}_btn_agregar_adicional`);
        const descInput = document.getElementById(`${prefix}_adicional_descripcion`);
        const precioInput = document.getElementById(`${prefix}_adicional_precio`);
        const cantInput = document.getElementById(`${prefix}_adicional_cantidad`);
        if (!btn) return;

        btn.addEventListener('click', function () {
            const descripcion = (descInput.value || '').trim();
            if (!descripcion) {
                alert('Ingrese una descripción para el ítem');
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

    const gestorAdicionalesCrear = crearGestorAdicionales('crear_sesion');
    enlazarFormularioAdicional('crear_sesion', gestorAdicionalesCrear);
    window.gestorAdicionalesCrearSesion = gestorAdicionalesCrear;

    const gestorAdicionalesEditar = crearGestorAdicionales('editar_sesion');
    enlazarFormularioAdicional('editar_sesion', gestorAdicionalesEditar);
    window.gestorAdicionalesEditarSesion = gestorAdicionalesEditar;

    window.cargarAdicionalesEditarSesion = function (adicionales) {
        gestorAdicionalesEditar.setItems(adicionales || []);
    };

    window.mostrarItemsVerSesion = function (adicionalesStr, totalFallback) {
        const cuerpo = document.getElementById('verSesionItemsDetallesBody');
        const totalSpan = document.getElementById('verSesionTotal');
        if (!cuerpo) return;

        cuerpo.innerHTML = '';
        let total = 0;

        if (adicionalesStr) {
            adicionalesStr.split(';').forEach(function (item) {
                const parts = item.split('|');
                if (parts.length === 3) {
                    const descripcion = parts[0];
                    const precioUnitario = parseFloat((parts[1] || '0').replace(',', '.')) || 0;
                    const cantidad = parseInt(parts[2]) || 1;
                    const subtotal = precioUnitario * cantidad;
                    total += subtotal;

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

        if (!total && totalFallback) {
            total = parseFloat(totalFallback) || 0;
        }

        if (totalSpan) totalSpan.textContent = total.toFixed(2);
    };

    const modalCrearSesion = document.getElementById('modalCrearSesion');
    if (modalCrearSesion) {
        modalCrearSesion.addEventListener('hidden.bs.modal', function () {
            gestorAdicionalesCrear.reset();
        });
    }
});
