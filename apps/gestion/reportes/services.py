from django.db.models import Sum, Count, Q
from django.utils import timezone

from apps.gestion.finanzas.models import Ingreso, Egreso, PagoEmpleado
from apps.gestion.clientes.models import Cliente
from apps.gestion.agenda.models import Cita
from apps.gestion.empleados.models import Empleado


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


def obtener_ingresos_reporte(fecha_inicio='', fecha_fin='', q='', categoria=''):
    from apps.gestion.pagos.models import Pago

    ingresos = list(Ingreso.objects.select_related('cliente', 'pago').all())
    pagos = Pago.objects.select_related('cliente', 'sesion', 'evento').filter(monto_pagado__gt=0)
    if fecha_inicio:
        ingresos = [i for i in ingresos if str(i.fecha) >= fecha_inicio]
        pagos = pagos.filter(fecha_pago__gte=fecha_inicio)
    if fecha_fin:
        ingresos = [i for i in ingresos if str(i.fecha) <= fecha_fin]
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
            cat = 'sesion_foto'
            concepto = f'Pago sesión: {pago.sesion}'
        elif pago.evento_id:
            cat = 'evento'
            concepto = f'Pago evento: {pago.evento}'
        else:
            cat = 'servicio'
            concepto = f'Pago de cliente: {pago.cliente}'
        ingresos_reporte.append(ReportEntry(
            fecha=pago.fecha_pago,
            concepto=concepto,
            categoria=cat,
            categoria_display=dict(Ingreso.CATEGORIA_CHOICES).get(cat, cat),
            monto=pago.monto_pagado,
            cliente=str(pago.cliente),
        ))

    if categoria:
        ingresos_reporte = [i for i in ingresos_reporte if i.categoria == categoria]
    if q:
        q_lower = q.lower()
        ingresos_reporte = [
            i for i in ingresos_reporte
            if q_lower in i.concepto.lower() or q_lower in str(i.cliente).lower()
        ]

    total = sum((item.monto for item in ingresos_reporte), 0)
    return ingresos_reporte, total


def obtener_egresos_reporte(fecha_inicio='', fecha_fin='', q='', categoria=''):
    egresos = Egreso.objects.all()
    pagos_empleados = PagoEmpleado.objects.select_related('empleado').all()
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
            cliente='-',
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

    if categoria:
        egresos_reporte = [e for e in egresos_reporte if e.categoria == categoria]
    if q:
        q_lower = q.lower()
        egresos_reporte = [
            e for e in egresos_reporte
            if q_lower in e.concepto.lower() or q_lower in str(e.cliente).lower()
        ]

    total = sum((item.monto for item in egresos_reporte), 0)
    return egresos_reporte, total


def obtener_clientes_reporte(q='', estado=''):
    clientes = Cliente.objects.annotate(
        total_citas=Count('citas'),
        total_ingresos=Sum('ingresos__monto'),
    )
    if estado:
        clientes = clientes.filter(estado=estado)
    if q:
        clientes = clientes.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(email__icontains=q) | Q(telefono__icontains=q)
        )
    return clientes


def obtener_citas_reporte(q='', estado='', fecha_inicio='', fecha_fin=''):
    citas = Cita.objects.select_related('cliente', 'empleado')
    if estado:
        citas = citas.filter(estado=estado)
    if fecha_inicio:
        citas = citas.filter(fecha__date__gte=fecha_inicio)
    if fecha_fin:
        citas = citas.filter(fecha__date__lte=fecha_fin)
    if q:
        citas = citas.filter(
            Q(cliente__nombre__icontains=q) | Q(cliente__apellido__icontains=q)
            | Q(empleado__nombre__icontains=q) | Q(ubicacion__icontains=q)
        )
    return citas


def obtener_empleados_reporte(q='', cargo='', estado=''):
    empleados = Empleado.objects.annotate(
        total_citas=Count('citas'),
        total_eventos=Count('eventos'),
        total_sesiones=Count('sesiones'),
    )
    if cargo:
        empleados = empleados.filter(cargo=cargo)
    if estado:
        empleados = empleados.filter(estado=estado)
    if q:
        empleados = empleados.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(email__icontains=q) | Q(telefono__icontains=q)
        )
    return empleados


def obtener_financiero_reporte(fecha_inicio='', fecha_fin=''):
    ingresos = Ingreso.objects.all()
    egresos = Egreso.objects.all()
    pagos_empleados = PagoEmpleado.objects.filter(estado__in=['pagado', 'parcial'])
    pagos_pendientes_qs = PagoEmpleado.objects.filter(estado__in=['pendiente', 'parcial'])

    if fecha_inicio:
        ingresos = ingresos.filter(fecha__gte=fecha_inicio)
        egresos = egresos.filter(fecha__gte=fecha_inicio)
        pagos_empleados = pagos_empleados.filter(fecha_pago__gte=fecha_inicio)
    if fecha_fin:
        ingresos = ingresos.filter(fecha__lte=fecha_fin)
        egresos = egresos.filter(fecha__lte=fecha_fin)
        pagos_empleados = pagos_empleados.filter(fecha_pago__lte=fecha_fin)

    total_ingresos = ingresos.aggregate(Sum('monto'))['monto__sum'] or 0
    total_egresos = egresos.aggregate(Sum('monto'))['monto__sum'] or 0
    total_pagos_empleados = pagos_empleados.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0
    total_egresos += total_pagos_empleados
    saldo_neto = total_ingresos - total_egresos
    pagos_pendientes = pagos_pendientes_qs.aggregate(Sum('total_a_pagar'))['total_a_pagar__sum'] or 0

    return {
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'saldo_neto': saldo_neto,
        'pagos_pendientes': pagos_pendientes,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'fecha_reporte': timezone.localdate(),
    }
