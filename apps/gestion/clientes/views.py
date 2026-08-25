from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cliente


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_clientes(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    clientes = Cliente.objects.all()
    if q:
        clientes = clientes.filter(
            Q(nombre__icontains=q)
            | Q(apellido__icontains=q)
            | Q(email__icontains=q)
            | Q(ci__icontains=q)
        )
    if estado:
        clientes = clientes.filter(estado=estado)

    paginator = Paginator(clientes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion/clientes/clientes.html', {'page_obj': page_obj, 'q': q, 'estado': estado})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_cliente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        ci = request.POST.get('ci', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        fecha_nacimiento = request.POST.get('fecha_nacimiento') or None
        observacion = request.POST.get('observacion', '').strip()

        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return redirect('clientes:listar_clientes')

        Cliente.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            ci=ci,
            ciudad=ciudad,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento,
            observacion=observacion,
        )
        messages.success(request, 'Cliente registrado correctamente.')
    return redirect('clientes:listar_clientes')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre', cliente.nombre).strip()
        cliente.apellido = request.POST.get('apellido', cliente.apellido).strip()
        cliente.email = request.POST.get('email', cliente.email).strip()
        cliente.telefono = request.POST.get('telefono', cliente.telefono).strip()
        cliente.ci = request.POST.get('ci', cliente.ci).strip()
        cliente.ciudad = request.POST.get('ciudad', cliente.ciudad).strip()
        cliente.direccion = request.POST.get('direccion', cliente.direccion).strip()
        cliente.fecha_nacimiento = request.POST.get('fecha_nacimiento') or cliente.fecha_nacimiento
        cliente.estado = request.POST.get('estado', cliente.estado)
        cliente.observacion = request.POST.get('observacion', cliente.observacion).strip()
        cliente.save()
        messages.success(request, 'Cliente actualizado correctamente.')
    return redirect('clientes:listar_clientes')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado correctamente.')
    return redirect('clientes:listar_clientes')
