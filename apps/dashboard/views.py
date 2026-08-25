from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from apps.gestion.clientes.models import Cliente
from apps.gestion.servicios.models import Servicio
from apps.gestion.empleados.models import Empleado
from apps.gestion.sesiones.models import Sesion
from apps.gestion.pagos.models import Pago


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def dashboard(request):
    total_clientes = Cliente.objects.count()
    clientes_activos = Cliente.objects.filter(estado='activo').count()
    total_servicios = Servicio.objects.filter(estado='activo').count()
    total_empleados = Empleado.objects.filter(estado='activo').count()
    sesiones_pendientes = Sesion.objects.filter(estado='pendiente').count()
    sesiones_confirmadas = Sesion.objects.filter(estado='confirmada').count()
    pagos_pendientes = Pago.objects.filter(estado='pendiente').count()

    return render(request, 'dashboard/dashboard.html', {
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'total_servicios': total_servicios,
        'total_empleados': total_empleados,
        'sesiones_pendientes': sesiones_pendientes,
        'sesiones_confirmadas': sesiones_confirmadas,
        'pagos_pendientes': pagos_pendientes,
    })
