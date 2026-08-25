from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Empleado


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_empleados(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    empleados = Empleado.objects.all()
    if q:
        empleados = empleados.filter(
            Q(nombre__icontains=q) | Q(apellido__icontains=q) | Q(email__icontains=q)
        )
    if estado:
        empleados = empleados.filter(estado=estado)

    paginator = Paginator(empleados, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion/empleados/empleados.html', {'page_obj': page_obj, 'q': q, 'estado': estado})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_empleado(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        cargo = request.POST.get('cargo', 'fotografo')
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        observacion = request.POST.get('observacion', '').strip()

        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return redirect('empleados:listar_empleados')

        Empleado.objects.create(
            nombre=nombre,
            apellido=apellido,
            cargo=cargo,
            telefono=telefono,
            email=email,
            observacion=observacion,
        )
        messages.success(request, 'Empleado registrado correctamente.')
    return redirect('empleados:listar_empleados')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre', empleado.nombre).strip()
        empleado.apellido = request.POST.get('apellido', empleado.apellido).strip()
        empleado.cargo = request.POST.get('cargo', empleado.cargo)
        empleado.telefono = request.POST.get('telefono', empleado.telefono).strip()
        empleado.email = request.POST.get('email', empleado.email).strip()
        empleado.estado = request.POST.get('estado', empleado.estado)
        empleado.observacion = request.POST.get('observacion', empleado.observacion).strip()
        empleado.save()
        messages.success(request, 'Empleado actualizado correctamente.')
    return redirect('empleados:listar_empleados')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_empleado(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado correctamente.')
    return redirect('empleados:listar_empleados')
