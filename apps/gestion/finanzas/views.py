from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Ingreso, Egreso, Caja, PagoEmpleado, ServicioBasico
from apps.gestion.empleados.models import Empleado


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def finanzas_dashboard(request):
    hoy = timezone.now().date()
    mes_actual = hoy.strftime('%m/%Y')

    total_ingresos_mes = Ingreso.objects.filter(fecha__month=hoy.month, fecha__year=hoy.year).aggregate(Sum('monto'))['monto__sum'] or 0
    total_egresos_mes = Egreso.objects.filter(fecha__month=hoy.month, fecha__year=hoy.year).aggregate(Sum('monto'))['monto__sum'] or 0
    saldo_mes = total_ingresos_mes - total_egresos_mes

    pagos_pendientes = PagoEmpleado.objects.filter(estado__in=['pendiente', 'parcial']).aggregate(Sum('total_a_pagar'))['total_a_pagar__sum'] or 0

    egresos = Egreso.objects.order_by('-fecha', '-id')
    paginator = Paginator(egresos, 10)

    return render(request, 'gestion/finanzas/finanzas.html', {
        'total_ingresos_mes': total_ingresos_mes,
        'total_egresos_mes': total_egresos_mes,
        'saldo_mes': saldo_mes,
        'pagos_pendientes': pagos_pendientes,
        'mes_actual': mes_actual,
        'page_obj': paginator.get_page(request.GET.get('page')),
        'categorias_egreso': Egreso.CATEGORIA_CHOICES,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_egreso(request):
    if request.method == 'POST':
        concepto = request.POST.get('concepto', '').strip()
        monto = request.POST.get('monto', '').strip()
        if concepto and monto:
            Egreso.objects.create(
                categoria=request.POST.get('categoria', 'otro'),
                concepto=concepto,
                monto=monto,
                fecha=request.POST.get('fecha') or timezone.now().date(),
                comprobante=request.POST.get('comprobante', '').strip(),
                notas=request.POST.get('notas', '').strip(),
            )
    return redirect('finanzas:finanzas_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_egreso(request, pk):
    egreso = get_object_or_404(Egreso, pk=pk)
    if request.method == 'POST':
        egreso.categoria = request.POST.get('categoria', egreso.categoria)
        egreso.concepto = request.POST.get('concepto', egreso.concepto).strip()
        egreso.monto = request.POST.get('monto', egreso.monto)
        egreso.fecha = request.POST.get('fecha') or egreso.fecha
        egreso.comprobante = request.POST.get('comprobante', '').strip()
        egreso.notas = request.POST.get('notas', '').strip()
        egreso.save()
    return redirect('finanzas:finanzas_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_egreso(request, pk):
    egreso = get_object_or_404(Egreso, pk=pk)
    if request.method == 'POST':
        egreso.delete()
    return redirect('finanzas:finanzas_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_pagos_empleados(request):
    pagos = PagoEmpleado.objects.select_related('empleado').all()
    return render(request, 'gestion/finanzas/pagos_empleados/pagos_empleados.html', {
        'pagos': pagos,
        'empleados': Empleado.objects.filter(estado='activo').order_by('nombre', 'apellido'),
        'estados': PagoEmpleado.ESTADO_CHOICES,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_pago_empleado(request):
    if request.method == 'POST':
        base = request.POST.get('monto_base') or 0
        bonificacion = request.POST.get('bonificacion') or 0
        descuentos = request.POST.get('descuentos') or 0
        total = request.POST.get('total_a_pagar') or base
        PagoEmpleado.objects.create(
            empleado_id=request.POST.get('empleado_id'),
            mes_año=request.POST.get('mes_año', '').strip(),
            monto_base=base,
            bonificación=bonificacion,
            descuentos=descuentos,
            total_a_pagar=total,
            monto_pagado=request.POST.get('monto_pagado') or 0,
            fecha_pago=request.POST.get('fecha_pago') or None,
            estado=request.POST.get('estado', 'pendiente'),
            comprobante=request.POST.get('comprobante', '').strip(),
            notas=request.POST.get('notas', '').strip(),
        )
    return redirect('finanzas:listar_pagos_empleados')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_pago_empleado(request, pk):
    pago = get_object_or_404(PagoEmpleado, pk=pk)
    if request.method == 'POST':
        pago.empleado_id = request.POST.get('empleado_id')
        pago.mes_año = request.POST.get('mes_año', '').strip()
        pago.monto_base = request.POST.get('monto_base') or 0
        pago.bonificación = request.POST.get('bonificacion') or 0
        pago.descuentos = request.POST.get('descuentos') or 0
        pago.total_a_pagar = request.POST.get('total_a_pagar') or 0
        pago.monto_pagado = request.POST.get('monto_pagado') or 0
        pago.fecha_pago = request.POST.get('fecha_pago') or None
        pago.estado = request.POST.get('estado', 'pendiente')
        pago.comprobante = request.POST.get('comprobante', '').strip()
        pago.notas = request.POST.get('notas', '').strip()
        pago.save()
    return redirect('finanzas:listar_pagos_empleados')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def anular_pago_empleado(request, pk):
    pago = get_object_or_404(PagoEmpleado, pk=pk)
    if request.method == 'POST':
        pago.estado = 'anulado'
        pago.save()
    return redirect('finanzas:listar_pagos_empleados')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def amortizar_pago_empleado(request, pk):
    pago = get_object_or_404(PagoEmpleado, pk=pk)
    if request.method == 'POST':
        monto_amortizar = float(request.POST.get('monto_amortizar') or 0)
        pago.monto_pagado += monto_amortizar
        pago.fecha_pago = request.POST.get('fecha_amortizacion') or pago.fecha_pago
        if pago.monto_pagado >= pago.total_a_pagar:
            pago.estado = 'pagado'
        elif pago.monto_pagado > 0:
            pago.estado = 'parcial'
        pago.save()
    return redirect('finanzas:listar_pagos_empleados')
