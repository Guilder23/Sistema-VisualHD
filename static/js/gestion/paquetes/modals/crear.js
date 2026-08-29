document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalCrearPaquete');
    if (!modal) return;
    
    let detalles = [];

    modal.addEventListener('hidden.bs.modal', function () {
        modal.querySelector('form').reset();
        detalles = [];
        actualizarTablaDetalles();
    });

    const btnAgregar = document.getElementById('btnAgregarDetalle');
    const descripcionInput = document.getElementById('crear_descripcion_detalle');
    const precioInput = document.getElementById('crear_precio_detalle');
    const cantidadInput = document.getElementById('crear_cantidad_detalle');

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

    function actualizarTablaDetalles() {
        const tbody = document.getElementById('tbodyDetallesCrear');
        tbody.innerHTML = '';
        let total = 0;

        detalles.forEach((detalle, index) => {
            const subtotal = detalle.precio_unitario * detalle.cantidad;
            total += subtotal;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td><input type="text" class="form-control form-control-sm input-descripcion" data-index="${index}" value="${detalle.descripcion}"></td>
                <td><input type="number" class="form-control form-control-sm input-precio" data-index="${index}" value="${detalle.precio_unitario}" step="0.01" min="0"></td>
                <td><input type="number" class="form-control form-control-sm input-cantidad" data-index="${index}" value="${detalle.cantidad}" min="1"></td>
                <td class="subtotal-cell">Bs ${subtotal.toFixed(2)}</td>
                <td><button type="button" class="btn btn-danger btn-sm btn-eliminar-detalle" data-index="${index}"><i class="fas fa-trash"></i></button></td>
            `;
            tbody.appendChild(row);
        });

        document.getElementById('crear_total').textContent = total.toFixed(2);
        document.getElementById('crear_precio_total').value = total.toFixed(2);
        document.getElementById('crear_detalles_json').value = JSON.stringify(detalles);

        // Agregar eventos a los nuevos inputs
        tbody.querySelectorAll('.input-descripcion').forEach(input => {
            input.addEventListener('change', function () {
                const index = this.dataset.index;
                detalles[index].descripcion = this.value;
            });
        });

        tbody.querySelectorAll('.input-precio').forEach(input => {
            input.addEventListener('change', function () {
                const index = this.dataset.index;
                detalles[index].precio_unitario = parseFloat(this.value) || 0;
                actualizarTablaDetalles();
            });
        });

        tbody.querySelectorAll('.input-cantidad').forEach(input => {
            input.addEventListener('change', function () {
                const index = this.dataset.index;
                detalles[index].cantidad = parseInt(this.value) || 1;
                actualizarTablaDetalles();
            });
        });

        tbody.querySelectorAll('.btn-eliminar-detalle').forEach(btn => {
            btn.addEventListener('click', function () {
                const index = this.dataset.index;
                detalles.splice(index, 1);
                actualizarTablaDetalles();
            });
        });
    }

    // Enviar detalles JSON al formulario
    document.getElementById('formCrearPaquete').addEventListener('submit', function () {
        document.getElementById('crear_detalles_json').value = JSON.stringify(detalles);
    });
});
