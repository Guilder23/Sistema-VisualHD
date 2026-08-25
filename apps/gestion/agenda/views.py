from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cita
from apps.gestion.clientes.models import Cliente
from apps.gestion.empleados.models import Empleado
from apps.gestion.sesiones.models import Sesion


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_citas(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    citas = Cita.objects.select_related('cliente', 'empleado', 'sesion').all()
    if q:
        citas = citas.filter(Q(cliente__nombre__icontains=q) | Q(cliente__apellido__icontains=q))
    if estado:
        citas = citas.filter(estado=estado)

    paginator = Paginator(citas, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion/agenda/agenda.html', {
        'page_obj': page_obj,
        'q': q,
        'estado': estado,
        'clientes': Cliente.objects.filter(estado='activo').order_by('nombre'),
        'empleados': Empleado.objects.filter(estado='activo').order_by('nombre'),
        'citas_calendario': citas,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_cita(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        empleado_id = request.POST.get('empleado_id')
        fecha = request.POST.get('fecha')
        duracion = request.POST.get('duracion_minutos') or 60
        descripcion = request.POST.get('descripcion', '').strip()
        ubicacion = request.POST.get('ubicacion', '').strip()
        notas = request.POST.get('notas', '').strip()

        cliente = Cliente.objects.filter(id=cliente_id).first()
        if not cliente:
            return redirect('agenda:listar_citas')

        Cita.objects.create(
            cliente=cliente,
            empleado_id=empleado_id or None,
            fecha=fecha,
            duracion_minutos=duracion,
            descripcion=descripcion,
            ubicacion=ubicacion,
            notas=notas,
        )
    return redirect('agenda:listar_citas')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        empleado_id = request.POST.get('empleado_id')
        if cliente_id:
            cita.cliente_id = cliente_id
        cita.empleado_id = empleado_id or None
        cita.fecha = request.POST.get('fecha') or cita.fecha
        cita.duracion_minutos = request.POST.get('duracion_minutos') or cita.duracion_minutos
        cita.estado = request.POST.get('estado', cita.estado)
        cita.descripcion = request.POST.get('descripcion', cita.descripcion).strip()
        cita.ubicacion = request.POST.get('ubicacion', cita.ubicacion).strip()
        cita.notas = request.POST.get('notas', cita.notas).strip()
        cita.save()
    return redirect('agenda:listar_citas')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)
    if request.method == 'POST':
        cita.delete()
    return redirect('agenda:listar_citas')
