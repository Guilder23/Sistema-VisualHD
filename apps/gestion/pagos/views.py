from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from .models import Pago
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


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_pagos(request):
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()

    # Obtener sesiones pendientes de pago
    sesiones_pendientes = []
    for sesion in Sesion.objects.select_related('cliente').all():
        pagos_sesion = Pago.objects.filter(sesion=sesion)
        total_pagado = sum(p.monto_pagado for p in pagos_sesion)
        pendiente = sesion.precio - total_pagado
        if pendiente > 0:
            sesiones_pendientes.append({
                'tipo': 'sesion',
                'objeto': sesion,
                'cliente': sesion.cliente,
                'total': sesion.precio,
                'pagado': total_pagado,
                'pendiente': pendiente,
                'pagos': pagos_sesion,
            })

    # Obtener eventos pendientes de pago
    eventos_pendientes = []
    for evento in Evento.objects.select_related('cliente').all():
        pagos_evento = Pago.objects.filter(evento=evento)
        total_pagado = sum(p.monto_pagado for p in pagos_evento)
        pendiente = evento.presupuesto - total_pagado
        if pendiente > 0:
            eventos_pendientes.append({
                'tipo': 'evento',
                'objeto': evento,
                'cliente': evento.cliente,
                'total': evento.presupuesto,
                'pagado': total_pagado,
                'pendiente': pendiente,
                'pagos': pagos_evento,
            })

    # Combinar y filtrar
    pendientes = sesiones_pendientes + eventos_pendientes
    
    if q:
        pendientes = [p for p in pendientes if q.lower() in str(p['cliente']).lower()]
    
    if tipo:
        pendientes = [p for p in pendientes if p['tipo'] == tipo]

    # Ordenar por pendiente descendente
    pendientes.sort(key=lambda x: x['pendiente'], reverse=True)

    paginator = Paginator(pendientes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'gestion/pagos/pagos.html', {
        'page_obj': page_obj,
        'q': q,
        'tipo': tipo,
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
                    monto=sesion.precio,
                    monto_pagado=Decimal('0'),
                    metodo_pago=metodo_pago,
                    fecha_pago=fecha_amortizacion,
                    estado='pendiente',
                    observacion=observacion,
                )
            pago.monto_pagado += monto_amortizar
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
            pago.monto_pagado += monto_amortizar
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
    return redirect('pagos:listar_pagos')
