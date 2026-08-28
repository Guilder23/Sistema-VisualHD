from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from .models import Pago
from .pdf import generar_pdf_cobro
from apps.gestion.clientes.models import Cliente
from apps.gestion.sesiones.models import Sesion
from apps.gestion.eventos.models import Evento
from apps.gestion.finanzas.models import Ingreso


def to_decimal(value, default=Decimal('0')):
    if value in (None, '',):
        return default
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return default


def sincronizar_ingreso(pago):
    if pago.estado != 'pagado':
        Ingreso.objects.filter(pago=pago).delete()
        return
    categoria = 'sesion_foto' if pago.sesion_id else ('evento' if pago.evento_id else 'servicio')
    concepto = f'Pago de cliente: {pago.cliente}'
    if pago.sesion:
        concepto = f'Pago sesión: {pago.sesion}'
    elif pago.evento:
        concepto = f'Pago evento: {pago.evento}'
    ingreso, _ = Ingreso.objects.update_or_create(
        pago=pago,
        defaults={
            'cliente': pago.cliente,
            'categoria': categoria,
            'concepto': concepto,
            'monto': pago.monto_pagado if pago.monto_pagado > 0 else pago.monto,
            'fecha': pago.fecha_pago,
            'referencia': f'Pago #{pago.pk}',
            'notas': pago.observacion,
        },
    )
    return ingreso


def _obtener_cobros(q='', tipo='', tab='pendientes'):
    cobros = []

    for sesion in Sesion.objects.select_related('cliente').prefetch_related('adicionales').all():
        pagos_sesion = Pago.objects.filter(sesion=sesion).order_by('-fecha_pago')
        total_pagado = sum(p.monto_pagado for p in pagos_sesion)
        total_sesion = sesion.total_general()
        pendiente = total_sesion - total_pagado
        es_pendiente = pendiente > 0
        if (tab == 'pendientes' and es_pendiente) or (tab == 'completados' and not es_pendiente and total_pagado > 0):
            cobros.append({
                'tipo': 'sesion',
                'objeto': sesion,
                'cliente': sesion.cliente,
                'total': total_sesion,
                'pagado': total_pagado,
                'pendiente': pendiente,
                'pagos': pagos_sesion,
            })

    for evento in Evento.objects.select_related('cliente').all():
        pagos_evento = Pago.objects.filter(evento=evento).order_by('-fecha_pago')
        total_pagado = sum(p.monto_pagado for p in pagos_evento)
        pendiente = evento.presupuesto - total_pagado
        es_pendiente = pendiente > 0
        if (tab == 'pendientes' and es_pendiente) or (tab == 'completados' and not es_pendiente and total_pagado > 0):
            cobros.append({
                'tipo': 'evento',
                'objeto': evento,
                'cliente': evento.cliente,
                'total': evento.presupuesto,
                'pagado': total_pagado,
                'pendiente': pendiente,
                'pagos': pagos_evento,
            })

    if q:
        cobros = [p for p in cobros if q.lower() in str(p['cliente']).lower()]

    if tipo:
        cobros = [p for p in cobros if p['tipo'] == tipo]

    if tab == 'pendientes':
        cobros.sort(key=lambda x: x['pendiente'], reverse=True)
    else:
        cobros.sort(key=lambda x: x['pagado'], reverse=True)

    return cobros


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_pagos(request):
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    tab = request.GET.get('tab', 'pendientes').strip()
    if tab not in ('pendientes', 'completados'):
        tab = 'pendientes'

    cobros = _obtener_cobros(q=q, tipo=tipo, tab=tab)

    paginator = Paginator(cobros, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    qs_sin_page = request.GET.copy()
    qs_sin_page.pop('page', None)

    return render(request, 'gestion/pagos/pagos.html', {
        'page_obj': page_obj,
        'q': q,
        'tipo': tipo,
        'tab': tab,
        'querystring': qs_sin_page.urlencode(),
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_pago(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        sesion_id = request.POST.get('sesion_id')
        evento_id = request.POST.get('evento_id')
        monto = to_decimal(request.POST.get('monto'))
        monto_pagado = to_decimal(request.POST.get('monto_pagado'))
        metodo_pago = request.POST.get('metodo_pago', 'efectivo')
        fecha_pago = request.POST.get('fecha_pago') or None
        estado = request.POST.get('estado', 'pendiente')
        observacion = request.POST.get('observacion', '').strip()

        cliente = Cliente.objects.filter(id=cliente_id).first()
        if not cliente:
            messages.error(request, 'Selecciona un cliente válido.')
            return redirect('pagos:listar_pagos')

        # Determinar estado basado en monto_pagado
        if monto_pagado and monto_pagado >= monto:
            estado = 'pagado'
        elif monto_pagado and monto_pagado > 0:
            estado = 'parcial'

        pago = Pago.objects.create(
            cliente=cliente,
            sesion_id=sesion_id or None,
            evento_id=evento_id or None,
            monto=monto,
            monto_pagado=monto_pagado,
            metodo_pago=metodo_pago,
            fecha_pago=fecha_pago or timezone.now().date(),
            estado=estado,
            observacion=observacion,
        )
        sincronizar_ingreso(pago)
        messages.success(request, 'Pago registrado correctamente.')
    return redirect('pagos:listar_pagos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        sesion_id = request.POST.get('sesion_id')
        evento_id = request.POST.get('evento_id')

        if cliente_id:
            pago.cliente_id = cliente_id
        pago.sesion_id = sesion_id or None
        pago.evento_id = evento_id or None
        pago.monto = to_decimal(request.POST.get('monto'), pago.monto)
        pago.monto_pagado = to_decimal(request.POST.get('monto_pagado'), pago.monto_pagado)
        pago.metodo_pago = request.POST.get('metodo_pago', pago.metodo_pago)
        pago.estado = request.POST.get('estado', pago.estado)
        pago.fecha_pago = request.POST.get('fecha_pago') or pago.fecha_pago
        pago.observacion = request.POST.get('observacion', pago.observacion).strip()

        # Actualizar estado basado en monto_pagado
        if pago.monto_pagado >= pago.monto:
            pago.estado = 'pagado'
        elif pago.monto_pagado > 0:
            pago.estado = 'parcial'

        pago.save()
        sincronizar_ingreso(pago)
        messages.success(request, 'Pago actualizado correctamente.')
    return redirect('pagos:listar_pagos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk)
    if request.method == 'POST':
        Ingreso.objects.filter(pago=pago).delete()
        pago.delete()
        messages.success(request, 'Pago eliminado correctamente.')
    return redirect('pagos:listar_pagos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def amortizar_pago(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        objeto_id = request.POST.get('objeto_id')
        monto_amortizar = to_decimal(request.POST.get('monto_amortizar'))
        metodo_pago = request.POST.get('metodo_pago', 'efectivo')
        fecha_amortizacion = request.POST.get('fecha_amortizacion') or timezone.now().date()
        observacion = request.POST.get('observacion', '').strip()

        if tipo == 'sesion':
            sesion = get_object_or_404(Sesion, pk=objeto_id)
            # Buscar o crear pago para esta sesión
            pago = Pago.objects.filter(sesion=sesion).first()
            if not pago:
                pago = Pago.objects.create(
                    cliente=sesion.cliente,
                    sesion=sesion,
                    monto=sesion.total_general(),
                    monto_pagado=Decimal('0'),
                    metodo_pago=metodo_pago,
                    fecha_pago=fecha_amortizacion,
                    estado='pendiente',
                    observacion=observacion,
                )
            pago.monto_pagado = Decimal(str(pago.monto_pagado)) + monto_amortizar
            pago.metodo_pago = metodo_pago
            pago.fecha_pago = fecha_amortizacion
            if observacion:
                pago.observacion = observacion
            if pago.monto_pagado >= pago.monto:
                pago.estado = 'pagado'
            elif pago.monto_pagado > 0:
                pago.estado = 'parcial'
            pago.save()
            sincronizar_ingreso(pago)
            messages.success(request, 'Amortización registrada correctamente.')
        elif tipo == 'evento':
            evento = get_object_or_404(Evento, pk=objeto_id)
            # Buscar o crear pago para este evento
            pago = Pago.objects.filter(evento=evento).first()
            if not pago:
                pago = Pago.objects.create(
                    cliente=evento.cliente,
                    evento=evento,
                    monto=evento.presupuesto,
                    monto_pagado=Decimal('0'),
                    metodo_pago=metodo_pago,
                    fecha_pago=fecha_amortizacion,
                    estado='pendiente',
                    observacion=observacion,
                )
            pago.monto_pagado = Decimal(str(pago.monto_pagado)) + monto_amortizar
            pago.metodo_pago = metodo_pago
            pago.fecha_pago = fecha_amortizacion
            if observacion:
                pago.observacion = observacion
            if pago.monto_pagado >= pago.monto:
                pago.estado = 'pagado'
            elif pago.monto_pagado > 0:
                pago.estado = 'parcial'
            pago.save()
            sincronizar_ingreso(pago)
            messages.success(request, 'Amortización registrada correctamente.')
    tab = request.POST.get('tab', 'pendientes')
    return redirect(f"{reverse('pagos:listar_pagos')}?tab={tab}")


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def pdf_cobro(request, tipo, objeto_id):
    if tipo == 'sesion':
        objeto = get_object_or_404(
            Sesion.objects.select_related('cliente').prefetch_related('adicionales'),
            pk=objeto_id,
        )
        pagos = Pago.objects.filter(sesion=objeto).order_by('-fecha_pago')
        total = objeto.total_general()
    elif tipo == 'evento':
        objeto = get_object_or_404(Evento.objects.select_related('cliente'), pk=objeto_id)
        pagos = Pago.objects.filter(evento=objeto).order_by('-fecha_pago')
        total = objeto.presupuesto
    else:
        return redirect('pagos:listar_pagos')

    pagado = sum(p.monto_pagado for p in pagos)
    pendiente = total - pagado
    buffer = generar_pdf_cobro(tipo, objeto, pagos, total, pagado, pendiente)
    nombre = f'resumen_cobro_{tipo}_{objeto_id}.pdf'
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre}"'
    return response
