from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Pago
from apps.gestion.clientes.models import Cliente
from apps.gestion.sesiones.models import Sesion
from apps.gestion.finanzas.models import Ingreso


def sincronizar_ingreso(pago):
    if pago.estado != 'pagado':
        Ingreso.objects.filter(pago=pago).delete()
        return
    ingreso, _ = Ingreso.objects.update_or_create(
        pago=pago,
        defaults={
            'cliente': pago.cliente,
            'categoria': 'sesion_foto' if pago.sesion_id else 'servicio',
            'concepto': f'Pago de cliente: {pago.cliente}',
            'monto': pago.monto,
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
    estado = request.GET.get('estado', '').strip()

    pagos = Pago.objects.select_related('cliente', 'sesion').all()
    if q:
        pagos = pagos.filter(Q(cliente__nombre__icontains=q) | Q(cliente__apellido__icontains=q))
    if estado:
        pagos = pagos.filter(estado=estado)

    paginator = Paginator(pagos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion/pagos/pagos.html', {
        'page_obj': page_obj,
        'q': q,
        'estado': estado,
        'clientes': Cliente.objects.filter(estado='activo').order_by('nombre'),
        'sesiones': Sesion.objects.all().order_by('-fecha'),
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_pago(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        sesion_id = request.POST.get('sesion_id')
        monto = request.POST.get('monto') or 0
        metodo_pago = request.POST.get('metodo_pago', 'efectivo')
        fecha_pago = request.POST.get('fecha_pago') or None
        estado = request.POST.get('estado', 'pagado')
        observacion = request.POST.get('observacion', '').strip()

        cliente = Cliente.objects.filter(id=cliente_id).first()
        if not cliente:
            messages.error(request, 'Selecciona un cliente válido.')
            return redirect('pagos:listar_pagos')

        pago = Pago.objects.create(
            cliente=cliente,
            sesion_id=sesion_id or None,
            monto=monto,
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

        if cliente_id:
            pago.cliente_id = cliente_id
        pago.sesion_id = sesion_id or None
        pago.monto = request.POST.get('monto') or pago.monto
        pago.metodo_pago = request.POST.get('metodo_pago', pago.metodo_pago)
        pago.estado = request.POST.get('estado', pago.estado)
        pago.fecha_pago = request.POST.get('fecha_pago') or pago.fecha_pago
        pago.observacion = request.POST.get('observacion', pago.observacion).strip()
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
