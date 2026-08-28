// Vista de calendario (mes/semana/día) para Gestión de Eventos
document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.getElementById('eventosVistaTabs');
    const vistaLista = document.getElementById('eventosVistaLista');
    const vistaCalendario = document.getElementById('eventosVistaCalendario');
    const calendarioEl = document.getElementById('calendarioEventos');
    if (!tabs || !vistaLista || !vistaCalendario || !calendarioEl) return;

    let calendar = null;

    function crearCalendario(vistaInicial) {
        if (calendar) {
            calendar.changeView(vistaInicial);
            return;
        }
        calendar = new FullCalendar.Calendar(calendarioEl, {
            locale: 'es',
            initialView: vistaInicial,
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: ''
            },
            height: 650,
            events: function (info, successCallback, failureCallback) {
                fetch(window.EVENTOS_CALENDARIO_URL, { credentials: 'same-origin' })
                    .then(res => res.json())
                    .then(data => successCallback(data.eventos || []))
                    .catch(err => failureCallback(err));
            },
            eventClick: function (info) {
                const props = info.event.extendedProps;
                alert(
                    info.event.title + '\n' +
                    'Cliente: ' + (props.cliente || '-') + '\n' +
                    'Servicio: ' + (props.servicio || '-') + '\n' +
                    'Estado: ' + (props.estado || '-') + '\n' +
                    'Ubicación: ' + (props.ubicacion || '-')
                );
            }
        });
        calendar.render();
    }

    tabs.querySelectorAll('.nav-link').forEach(function (link) {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            tabs.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');

            const vista = this.dataset.vista;
            if (vista === 'lista') {
                vistaCalendario.style.display = 'none';
                vistaLista.style.display = 'block';
            } else {
                vistaLista.style.display = 'none';
                vistaCalendario.style.display = 'block';
                crearCalendario(vista);
                if (calendar) calendar.updateSize();
            }
        });
    });
});
