from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Sesion
from apps.gestion.clientes.models import Cliente
from apps.gestion.servicios.models import Servicio
from apps.gestion.empleados.models import Empleado


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_sesiones(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    sesiones = Sesion.objects.select_related('cliente', 'servicio', 'empleado').all()
    if q:
        sesiones = sesiones.filter(
            Q(cliente__nombre__icontains=q) | Q(cliente__apellido__icontains=q) | Q(lugar__icontains=q)
        )
    if estado:
        sesiones = sesiones.filter(estado=estado)

    paginator = Paginator(sesiones, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion/sesiones/sesiones.html', {
        'page_obj': page_obj,
        'q': q,
        'estado': estado,
        'clientes': Cliente.objects.filter(estado='activo').order_by('nombre'),
        'servicios': Servicio.objects.filter(estado='activo').order_by('nombre'),
        'empleados': Empleado.objects.filter(estado='activo').order_by('nombre'),
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_sesion(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        servicio_id = request.POST.get('servicio_id')
        empleado_id = request.POST.get('empleado_id')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        lugar = request.POST.get('lugar', '').strip()
        observacion = request.POST.get('observacion', '').strip()

        cliente = Cliente.objects.filter(id=cliente_id).first()
        if not cliente or not fecha or not hora:
            messages.error(request, 'Cliente, fecha y hora son obligatorios.')
            return redirect('sesiones:listar_sesiones')

        Sesion.objects.create(
            cliente=cliente,
            servicio_id=servicio_id or None,
            empleado_id=empleado_id or None,
            fecha=fecha,
            hora=hora,
            lugar=lugar,
            observacion=observacion,
        )
        messages.success(request, 'Sesión registrada correctamente.')
    return redirect('sesiones:listar_sesiones')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        servicio_id = request.POST.get('servicio_id')
        empleado_id = request.POST.get('empleado_id')

        if cliente_id:
            sesion.cliente_id = cliente_id
        sesion.servicio_id = servicio_id or None
        sesion.empleado_id = empleado_id or None
        sesion.fecha = request.POST.get('fecha') or sesion.fecha
        sesion.hora = request.POST.get('hora') or sesion.hora
        sesion.lugar = request.POST.get('lugar', sesion.lugar).strip()
        sesion.estado = request.POST.get('estado', sesion.estado)
        sesion.observacion = request.POST.get('observacion', sesion.observacion).strip()
        sesion.save()
        messages.success(request, 'Sesión actualizada correctamente.')
    return redirect('sesiones:listar_sesiones')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_sesion(request, pk):
    sesion = get_object_or_404(Sesion, pk=pk)
    if request.method == 'POST':
        sesion.delete()
        messages.success(request, 'Sesión eliminada correctamente.')
    return redirect('sesiones:listar_sesiones')
