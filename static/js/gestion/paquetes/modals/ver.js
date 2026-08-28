document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-ver-paquete').forEach(function (btn) {
        btn.addEventListener('click', function () {
            document.getElementById('ver_nombre').textContent = this.dataset.nombre || '-';
            document.getElementById('ver_servicio_principal').textContent = this.dataset.servicio_principal || '-';
            document.getElementById('ver_descripcion').textContent = this.dataset.descripcion || '-';
            document.getElementById('ver_precio').textContent = this.dataset.precio || '-';
            document.getElementById('ver_estado').textContent = this.dataset.estado || '-';
            document.getElementById('ver_creado').textContent = this.dataset.creado || '-';
            
            // Cargar detalles en la tabla
            const tbody = document.getElementById('tbodyDetallesVer');
            tbody.innerHTML = '';
            let total = 0;
            
            if (this.dataset.detalles && this.dataset.detalles !== '') {
                const detallesStr = this.dataset.detalles;
                const detallesArray = detallesStr.split(';');
                detallesArray.forEach(detalleStr => {
                    const parts = detalleStr.split('|');
                    if (parts.length === 3) {
                        const descripcion = parts[0];
                        const precioStr = parts[1].replace(',', '.');
                        const precioUnitario = parseFloat(precioStr) || 0;
                        const cantidad = parseInt(parts[2]) || 1;
                        const subtotal = precioUnitario * cantidad;
                        total += subtotal;
                        
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${descripcion}</td>
                            <td>Bs ${precioUnitario.toFixed(2)}</td>
                            <td>${cantidad}</td>
                            <td>Bs ${subtotal.toFixed(2)}</td>
                        `;
                        tbody.appendChild(row);
                    }
                });
            }
            
            document.getElementById('ver_total').textContent = total.toFixed(2);
        });
    });
});
