from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Evento
from apps.gestion.clientes.models import Cliente
from apps.gestion.empleados.models import Empleado
from apps.gestion.servicios.models import Servicio


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_eventos(request):
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    estado = request.GET.get('estado', '').strip()

    eventos = Evento.objects.select_related('cliente').prefetch_related('empleados_asignados').all()
    if q:
        eventos = eventos.filter(Q(nombre__icontains=q) | Q(cliente__nombre__icontains=q))
    if tipo:
        eventos = eventos.filter(tipo=tipo)
    if estado:
        eventos = eventos.filter(estado=estado)

    paginator = Paginator(eventos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion/eventos/eventos.html', {
        'page_obj': page_obj,
        'q': q,
        'tipo': tipo,
        'estado': estado,
        'clientes': Cliente.objects.filter(estado='activo'),
        'empleados': Empleado.objects.filter(estado='activo'),
        'servicios': Servicio.objects.filter(estado='activo').order_by('nombre'),
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_evento(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        nombre = request.POST.get('nombre', '').strip()
        tipo = request.POST.get('tipo', 'otro')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ubicacion = request.POST.get('ubicacion', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        presupuesto = request.POST.get('presupuesto') or 0
        notas = request.POST.get('notas', '').strip()

        cliente = Cliente.objects.filter(id=cliente_id).first()
        if not cliente:
            return redirect('eventos:listar_eventos')

        evento = Evento.objects.create(
            cliente=cliente,
            nombre=nombre,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            ubicacion=ubicacion,
            descripcion=descripcion,
            presupuesto=presupuesto,
            notas=notas,
        )
    return redirect('eventos:listar_eventos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        if cliente_id:
            evento.cliente_id = cliente_id
        evento.nombre = request.POST.get('nombre', evento.nombre).strip()
        evento.tipo = request.POST.get('tipo', evento.tipo)
        evento.fecha_inicio = request.POST.get('fecha_inicio') or evento.fecha_inicio
        evento.fecha_fin = request.POST.get('fecha_fin') or evento.fecha_fin
        evento.ubicacion = request.POST.get('ubicacion', evento.ubicacion).strip()
        evento.descripcion = request.POST.get('descripcion', evento.descripcion).strip()
        evento.presupuesto = request.POST.get('presupuesto', evento.presupuesto)
        evento.estado = request.POST.get('estado', evento.estado)
        evento.notas = request.POST.get('notas', evento.notas).strip()
        evento.save()
    return redirect('eventos:listar_eventos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.delete()
    return redirect('eventos:listar_eventos')
