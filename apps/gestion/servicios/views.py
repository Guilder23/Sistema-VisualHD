from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Servicio


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_servicios(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    servicios = Servicio.objects.all()
    if q:
        servicios = servicios.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    if estado:
        servicios = servicios.filter(estado=estado)

    paginator = Paginator(servicios, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion/servicios/servicios.html', {'page_obj': page_obj, 'q': q, 'estado': estado})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_servicio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio = request.POST.get('precio') or 0
        duracion_minutos = request.POST.get('duracion_minutos') or 60

        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return redirect('servicios:listar_servicios')

        Servicio.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            duracion_minutos=duracion_minutos,
        )
        messages.success(request, 'Servicio registrado correctamente.')
    return redirect('servicios:listar_servicios')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.nombre = request.POST.get('nombre', servicio.nombre).strip()
        servicio.descripcion = request.POST.get('descripcion', servicio.descripcion).strip()
        servicio.precio = request.POST.get('precio') or servicio.precio
        servicio.duracion_minutos = request.POST.get('duracion_minutos') or servicio.duracion_minutos
        servicio.estado = request.POST.get('estado', servicio.estado)
        servicio.save()
        messages.success(request, 'Servicio actualizado correctamente.')
    return redirect('servicios:listar_servicios')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        messages.success(request, 'Servicio eliminado correctamente.')
    return redirect('servicios:listar_servicios')
