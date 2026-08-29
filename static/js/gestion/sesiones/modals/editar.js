document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-editar-sesion').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const form = document.getElementById('formEditarSesion');
            form.action = this.dataset.action;
            form.querySelector('#editar_cliente_id').value = this.dataset.clienteId || '';
            form.querySelector('#editar_servicio_id').value = this.dataset.servicioId || '';
            form.querySelector('#editar_empleado_id').value = this.dataset.empleadoId || '';
            form.querySelector('#editar_fecha').value = this.dataset.fecha || '';
            form.querySelector('#editar_hora').value = this.dataset.hora || '';
            form.querySelector('#editar_lugar').value = this.dataset.lugar || '';
            form.querySelector('#editar_estado').value = this.dataset.estado || 'pendiente';
            form.querySelector('#editar_observacion').value = this.dataset.observacion || '';

            const adicionalesStr = this.dataset.adicionales || '';
            const adicionales = [];
            adicionalesStr.split(';').forEach(function (item) {
                const parts = String(item).split('|');
                if (parts.length === 3) {
                    adicionales.push({
                        descripcion: parts[0],
                        precio_unitario: parseFloat((parts[1] || '0').replace(',', '.')) || 0,
                        cantidad: parseInt(parts[2]) || 1
                    });
                }
            });

            if (typeof window.cargarAdicionalesEditarSesion === 'function') {
                window.cargarAdicionalesEditarSesion(adicionales);
            }
        });
    });
});
