from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q
from django.shortcuts import render
from django.utils import timezone

from apps.gestion.finanzas.models import Ingreso, Egreso, PagoEmpleado
from apps.gestion.clientes.models import Cliente
from apps.gestion.agenda.models import Cita
from apps.gestion.empleados.models import Empleado
from apps.gestion.pagos.models import Pago


class ReportEntry:
    def __init__(self, fecha, concepto, categoria, categoria_display, monto, cliente=None):
        self.fecha = fecha
        self.concepto = concepto
        self.categoria = categoria
        self.categoria_display = categoria_display
        self.monto = monto
        self.cliente = cliente

    def get_categoria_display(self):
        return self.categoria_display


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reportes_inicio(request):
    return render(request, 'gestion/reportes/reportes.html')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_ingresos(request):
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    ingresos = list(Ingreso.objects.select_related('cliente', 'pago').all())
    pagos = Pago.objects.select_related('cliente', 'sesion', 'evento').filter(monto_pagado__gt=0)
    if fecha_inicio:
        ingresos = [i for i in ingresos if i.fecha >= fecha_inicio]
        pagos = pagos.filter(fecha_pago__gte=fecha_inicio)
    if fecha_fin:
        ingresos = [i for i in ingresos if i.fecha <= fecha_fin]
        pagos = pagos.filter(fecha_pago__lte=fecha_fin)

    ingresos_reporte = []
    seen_pagos = set()
    for ingreso in ingresos:
        ingresos_reporte.append(ReportEntry(
            fecha=ingreso.fecha,
            concepto=ingreso.concepto,
            categoria=ingreso.categoria,
            categoria_display=ingreso.get_categoria_display(),
            monto=ingreso.monto,
            cliente=ingreso.cliente.nombre if ingreso.cliente else '-',
        ))
        if ingreso.pago_id:
            seen_pagos.add(ingreso.pago_id)

    for pago in pagos:
        if pago.pk in seen_pagos:
            continue
        if pago.sesion_id:
            categoria = 'sesion_foto'
            concepto = f'Pago sesión: {pago.sesion}'
        elif pago.evento_id:
            categoria = 'evento'
            concepto = f'Pago evento: {pago.evento}'
        else:
            categoria = 'servicio'
            concepto = f'Pago de cliente: {pago.cliente}'
        ingresos_reporte.append(ReportEntry(
            fecha=pago.fecha_pago,
            concepto=concepto,
            categoria=categoria,
            categoria_display=dict(Ingreso.CATEGORIA_CHOICES).get(categoria, categoria),
            monto=pago.monto_pagado,
            cliente=str(pago.cliente),
        ))

    total = sum((item.monto for item in ingresos_reporte), 0)
    por_categoria = {}
    for item in ingresos_reporte:
        por_categoria[item.categoria] = por_categoria.get(item.categoria, 0) + item.monto

    return render(request, 'gestion/reportes/ingresos.html', {
        'ingresos': ingresos_reporte,
        'total': total,
        'por_categoria': [{'categoria': key, 'total': value} for key, value in por_categoria.items()],
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_egresos(request):
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    egresos = Egreso.objects.all()
    pagos_empleados = PagoEmpleado.objects.all()
    if fecha_inicio:
        egresos = egresos.filter(fecha__gte=fecha_inicio)
        pagos_empleados = pagos_empleados.filter(fecha_pago__gte=fecha_inicio)
    if fecha_fin:
        egresos = egresos.filter(fecha__lte=fecha_fin)
        pagos_empleados = pagos_empleados.filter(fecha_pago__lte=fecha_fin)

    egresos_reporte = [
        ReportEntry(
            fecha=item.fecha,
            concepto=item.concepto,
            categoria=item.categoria,
            categoria_display=item.get_categoria_display(),
            monto=item.monto,
            cliente='-'
        ) for item in egresos
    ]
    egresos_reporte.extend([
        ReportEntry(
            fecha=item.fecha_pago,
            concepto=f'Pago a empleado: {item.empleado}',
            categoria='pago_empleado',
            categoria_display='Pago a empleado',
            monto=item.monto_pagado,
            cliente=str(item.empleado),
        ) for item in pagos_empleados if item.monto_pagado and item.estado != 'anulado'
    ])

    total = sum((item.monto for item in egresos_reporte), 0)
    por_categoria = {}
    for item in egresos_reporte:
        por_categoria[item.categoria] = por_categoria.get(item.categoria, 0) + item.monto

    return render(request, 'gestion/reportes/egresos.html', {
        'egresos': egresos_reporte,
        'total': total,
        'por_categoria': [{'categoria': key, 'total': value} for key, value in por_categoria.items()],
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
    total_pagos_empleados = PagoEmpleado.objects.filter(estado__in=['pagado', 'parcial']).aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0
    total_egresos += total_pagos_empleados
    saldo_neto = total_ingresos - total_egresos

    pagos_pendientes = PagoEmpleado.objects.filter(estado__in=['pendiente', 'parcial']).aggregate(Sum('total_a_pagar'))['total_a_pagar__sum'] or 0

    return render(request, 'gestion/reportes/financiero.html', {
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'saldo_neto': saldo_neto,
        'pagos_pendientes': pagos_pendientes,
    })
