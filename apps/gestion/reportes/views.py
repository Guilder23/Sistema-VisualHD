from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from django.utils import timezone

from apps.gestion.finanzas.models import Ingreso, Egreso, PagoEmpleado
from apps.gestion.clientes.models import Cliente
from apps.gestion.agenda.models import Cita
from apps.gestion.empleados.models import Empleado


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reportes_inicio(request):
    return render(request, 'gestion/reportes/reportes.html')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_ingresos(request):
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    ingresos = Ingreso.objects.all()
    if fecha_inicio:
        ingresos = ingresos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        ingresos = ingresos.filter(fecha__lte=fecha_fin)

    total = ingresos.aggregate(Sum('monto'))['monto__sum'] or 0
    por_categoria = ingresos.values('categoria').annotate(total=Sum('monto'))

    return render(request, 'gestion/reportes/ingresos.html', {
        'ingresos': ingresos,
        'total': total,
        'por_categoria': por_categoria,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_egresos(request):
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    egresos = Egreso.objects.all()
    if fecha_inicio:
        egresos = egresos.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        egresos = egresos.filter(fecha__lte=fecha_fin)

    total = egresos.aggregate(Sum('monto'))['monto__sum'] or 0
    por_categoria = egresos.values('categoria').annotate(total=Sum('monto'))

    return render(request, 'gestion/reportes/egresos.html', {
        'egresos': egresos,
        'total': total,
        'por_categoria': por_categoria,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_clientes(request):
    clientes = Cliente.objects.annotate(
        total_citas=Count('citas'),
        total_ingresos=Sum('ingresos__monto')
    )
    
    return render(request, 'gestion/reportes/clientes.html', {
        'clientes': clientes,
        'total_clientes': clientes.count(),
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_citas(request):
    citas = Cita.objects.select_related('cliente', 'empleado')
    estado = request.GET.get('estado', '')
    if estado:
        citas = citas.filter(estado=estado)

    return render(request, 'gestion/reportes/citas.html', {
        'citas': citas,
        'total': citas.count(),
        'estado': estado,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_empleados(request):
    empleados = Empleado.objects.annotate(
        total_citas=Count('citas'),
        total_eventos=Count('eventos')
    )
    
    return render(request, 'gestion/reportes/empleados.html', {
        'empleados': empleados,
        'total_empleados': empleados.count(),
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_financiero(request):
    hoy = timezone.now().date()
    
    total_ingresos = Ingreso.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    total_egresos = Egreso.objects.aggregate(Sum('monto'))['monto__sum'] or 0
    saldo_neto = total_ingresos - total_egresos
    
    pagos_pendientes = PagoEmpleado.objects.filter(estado__in=['pendiente', 'parcial']).aggregate(Sum('total_a_pagar'))['total_a_pagar__sum'] or 0

    return render(request, 'gestion/reportes/financiero.html', {
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'saldo_neto': saldo_neto,
        'pagos_pendientes': pagos_pendientes,
    })
