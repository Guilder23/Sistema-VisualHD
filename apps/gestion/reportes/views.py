from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

from apps.gestion.finanzas.models import Ingreso, Egreso
from apps.gestion.empleados.models import Empleado
from apps.gestion.agenda.models import Cita
from apps.gestion.clientes.models import Cliente

from .services import (
    obtener_ingresos_reporte,
    obtener_egresos_reporte,
    obtener_clientes_reporte,
    obtener_citas_reporte,
    obtener_empleados_reporte,
    obtener_financiero_reporte,
)
from .pdf import (
    generar_pdf_ingresos,
    generar_pdf_egresos,
    generar_pdf_clientes,
    generar_pdf_citas,
    generar_pdf_empleados,
    generar_pdf_financiero,
)


def _filtros_request(request):
    return {
        'q': request.GET.get('q', '').strip(),
        'estado': request.GET.get('estado', '').strip(),
        'categoria': request.GET.get('categoria', '').strip(),
        'cargo': request.GET.get('cargo', '').strip(),
        'fecha_inicio': request.GET.get('fecha_inicio', '').strip(),
        'fecha_fin': request.GET.get('fecha_fin', '').strip(),
    }


def _pick(filtros, *keys):
    return {k: filtros.get(k, '') for k in keys}


def _respuesta_pdf(buffer, nombre):
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre}"'
    return response


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reportes_inicio(request):
    return render(request, 'gestion/reportes/reportes.html')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_ingresos(request):
    filtros = _filtros_request(request)
    ingresos, total = obtener_ingresos_reporte()
    return render(request, 'gestion/reportes/ingresos.html', {
        'ingresos': ingresos,
        'total': total,
        'filtros': filtros,
        'categorias': Ingreso.CATEGORIA_CHOICES,
        'pdf_url': 'reportes:pdf_ingresos',
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def pdf_ingresos(request):
    filtros = _filtros_request(request)
    ingresos, total = obtener_ingresos_reporte(**_pick(filtros, 'fecha_inicio', 'fecha_fin', 'q', 'categoria'))
    buffer = generar_pdf_ingresos(ingresos, total, filtros)
    return _respuesta_pdf(buffer, 'reporte_ingresos.pdf')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_egresos(request):
    filtros = _filtros_request(request)
    egresos, total = obtener_egresos_reporte()
    categorias = list(Egreso.CATEGORIA_CHOICES) + [('pago_empleado', 'Pago a empleado')]
    return render(request, 'gestion/reportes/egresos.html', {
        'egresos': egresos,
        'total': total,
        'filtros': filtros,
        'categorias': categorias,
        'pdf_url': 'reportes:pdf_egresos',
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def pdf_egresos(request):
    filtros = _filtros_request(request)
    egresos, total = obtener_egresos_reporte(**_pick(filtros, 'fecha_inicio', 'fecha_fin', 'q', 'categoria'))
    buffer = generar_pdf_egresos(egresos, total, filtros)
    return _respuesta_pdf(buffer, 'reporte_egresos.pdf')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_clientes(request):
    filtros = _filtros_request(request)
    clientes = obtener_clientes_reporte()
    return render(request, 'gestion/reportes/clientes.html', {
        'clientes': clientes,
        'total_clientes': clientes.count(),
        'filtros': filtros,
        'pdf_url': 'reportes:pdf_clientes',
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def pdf_clientes(request):
    filtros = _filtros_request(request)
    clientes = obtener_clientes_reporte(**_pick(filtros, 'q', 'estado'))
    buffer = generar_pdf_clientes(clientes, filtros)
    return _respuesta_pdf(buffer, 'reporte_clientes.pdf')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_citas(request):
    filtros = _filtros_request(request)
    citas = obtener_citas_reporte()
    return render(request, 'gestion/reportes/citas.html', {
        'citas': citas,
        'total': citas.count(),
        'filtros': filtros,
        'estados': Cita.ESTADO_CHOICES,
        'pdf_url': 'reportes:pdf_citas',
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def pdf_citas(request):
    filtros = _filtros_request(request)
    citas = obtener_citas_reporte(**_pick(filtros, 'q', 'estado', 'fecha_inicio', 'fecha_fin'))
    buffer = generar_pdf_citas(citas, filtros)
    return _respuesta_pdf(buffer, 'reporte_citas.pdf')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_empleados(request):
    filtros = _filtros_request(request)
    empleados = obtener_empleados_reporte()
    return render(request, 'gestion/reportes/empleados.html', {
        'empleados': empleados,
        'total_empleados': empleados.count(),
        'filtros': filtros,
        'cargos': Empleado.CARGO_CHOICES,
        'estados': Empleado.ESTADO_CHOICES,
        'pdf_url': 'reportes:pdf_empleados',
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def pdf_empleados(request):
    filtros = _filtros_request(request)
    empleados = obtener_empleados_reporte(**_pick(filtros, 'q', 'cargo', 'estado'))
    buffer = generar_pdf_empleados(empleados, filtros)
    return _respuesta_pdf(buffer, 'reporte_empleados.pdf')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def reporte_financiero(request):
    filtros = _filtros_request(request)
    datos = obtener_financiero_reporte(
        fecha_inicio=filtros['fecha_inicio'],
        fecha_fin=filtros['fecha_fin'],
    )
    return render(request, 'gestion/reportes/financiero.html', {
        **datos,
        'filtros': filtros,
        'pdf_url': 'reportes:pdf_financiero',
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def pdf_financiero(request):
    filtros = _filtros_request(request)
    datos = obtener_financiero_reporte(**_pick(filtros, 'fecha_inicio', 'fecha_fin'))
    buffer = generar_pdf_financiero(datos, filtros)
    return _respuesta_pdf(buffer, 'reporte_financiero.pdf')
