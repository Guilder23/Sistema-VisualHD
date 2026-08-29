document.addEventListener('DOMContentLoaded', function () {
    let detalles = [];

    document.querySelectorAll('.btn-editar-paquete').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEditarPaquete');
            form.action = this.dataset.action;
            form.querySelector('#editar_nombre').value = this.dataset.nombre || '';
            form.querySelector('#editar_descripcion').value = this.dataset.descripcion || '';
            form.querySelector('#editar_precio_total').value = this.dataset.precio || '';
            form.querySelector('#editar_estado').value = this.dataset.estado || 'activo';
            form.querySelector('#editar_servicio_principal').value = this.dataset.servicio_principal || '';
            
            // Cargar detalles existentes desde data attribute
            detalles = [];
            if (this.dataset.detalles && this.dataset.detalles !== '') {
                const detallesStr = this.dataset.detalles;
                const detallesArray = detallesStr.split(';');
                detallesArray.forEach(detalleStr => {
                    const parts = detalleStr.split('|');
                    if (parts.length === 3) {
                        // Reemplazar coma por punto para el precio
                        const precioStr = parts[1].replace(',', '.');
                        detalles.push({
                            descripcion: parts[0],
                            precio_unitario: parseFloat(precioStr) || 0,
                            cantidad: parseInt(parts[2]) || 1
                        });
                    }
                });
            }
            actualizarTablaDetalles();
        });
    });

    const modal = document.getElementById('modalEditarPaquete');
    if (modal) {
        modal.addEventListener('hidden.bs.modal', function () {
            detalles = [];
            actualizarTablaDetalles();
        });
    }

    const btnAgregar = document.getElementById('btnAgregarDetalleEditar');
    const descripcionInput = document.getElementById('editar_descripcion_detalle');
    const precioInput = document.getElementById('editar_precio_detalle');
    const cantidadInput = document.getElementById('editar_cantidad_detalle');

    if (btnAgregar) {
        btnAgregar.addEventListener('click', function () {
            const descripcion = descripcionInput.value.trim();
            const precioUnitario = parseFloat(precioInput.value) || 0;
            const cantidad = parseInt(cantidadInput.value) || 1;
            
            if (!descripcion) {
                alert('Ingrese una descripción');
                return;
            }

            detalles.push({
                descripcion: descripcion,
                precio_unitario: precioUnitario,
                cantidad: cantidad
            });

            actualizarTablaDetalles();
            descripcionInput.value = '';
            precioInput.value = '';
            cantidadInput.value = 1;
        });
    }

    function actualizarTablaDetalles() {
        const tbody = document.getElementById('tbodyDetallesEditar');
        if (!tbody) return;
        
        tbody.innerHTML = '';
        let total = 0;

        detalles.forEach((detalle, index) => {
            const subtotal = detalle.precio_unitario * detalle.cantidad;
            total += subtotal;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td><input type="text" class="form-control form-control-sm input-descripcion-editar" data-index="${index}" value="${detalle.descripcion}"></td>
                <td><input type="number" class="form-control form-control-sm input-precio-editar" data-index="${index}" value="${detalle.precio_unitario}" step="0.01" min="0"></td>
                <td><input type="number" class="form-control form-control-sm input-cantidad-editar" data-index="${index}" value="${detalle.cantidad}" min="1"></td>
                <td class="subtotal-cell-editar">Bs ${subtotal.toFixed(2)}</td>
                <td><button type="button" class="btn btn-danger btn-sm btn-eliminar-detalle-editar" data-index="${index}"><i class="fas fa-trash"></i></button></td>
            `;
            tbody.appendChild(row);
        });

        document.getElementById('editar_total').textContent = total.toFixed(2);
        document.getElementById('editar_precio_total').value = total.toFixed(2);
        document.getElementById('editar_detalles_json').value = JSON.stringify(detalles);

        tbody.querySelectorAll('.input-descripcion-editar').forEach(input => {
            input.addEventListener('change', function () {
                const index = this.dataset.index;
                detalles[index].descripcion = this.value;
            });
        });

        tbody.querySelectorAll('.input-precio-editar').forEach(input => {
            input.addEventListener('change', function () {
                const index = this.dataset.index;
                detalles[index].precio_unitario = parseFloat(this.value) || 0;
                actualizarTablaDetalles();
            });
        });

        tbody.querySelectorAll('.input-cantidad-editar').forEach(input => {
            input.addEventListener('change', function () {
                const index = this.dataset.index;
                detalles[index].cantidad = parseInt(this.value) || 1;
                actualizarTablaDetalles();
            });
        });

        tbody.querySelectorAll('.btn-eliminar-detalle-editar').forEach(btn => {
            btn.addEventListener('click', function () {
                const index = this.dataset.index;
                detalles.splice(index, 1);
                actualizarTablaDetalles();
            });
        });
    }

    const formEditar = document.getElementById('formEditarPaquete');
    if (formEditar) {
        formEditar.addEventListener('submit', function () {
            document.getElementById('editar_detalles_json').value = JSON.stringify(detalles);
        });
    }
});
