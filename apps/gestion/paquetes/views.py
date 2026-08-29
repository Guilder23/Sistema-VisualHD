from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from decimal import Decimal

from .models import Paquete, DetallePaquete
from apps.gestion.servicios.models import Servicio


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_paquetes(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    paquetes = Paquete.objects.all()
    if q:
        paquetes = paquetes.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    if estado:
        paquetes = paquetes.filter(estado=estado)

    servicios = Servicio.objects.filter(estado='activo')

    paginator = Paginator(paquetes, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'gestion/paquetes/paquetes.html', {'page_obj': page_obj, 'q': q, 'estado': estado, 'servicios': servicios})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_paquete(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio_total = request.POST.get('precio_total') or 0
        estado = request.POST.get('estado', 'activo')
        servicio_principal_id = request.POST.get('servicio_principal')
        detalles_json = request.POST.get('detalles_json', '[]')

        if not nombre:
            messages.error(request, 'El nombre es obligatorio.')
            return redirect('paquetes:listar_paquetes')

        paquete = Paquete.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio_total=precio_total,
            estado=estado,
            servicio_principal_id=servicio_principal_id or None
        )

        # Procesar detalles del paquete
        import json
        try:
            detalles = json.loads(detalles_json)
            for detalle in detalles:
                DetallePaquete.objects.create(
                    paquete=paquete,
                    descripcion=detalle['descripcion'],
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio_unitario']
                )
        except (json.JSONDecodeError, KeyError):
            pass

        messages.success(request, 'Paquete registrado correctamente.')
    return redirect('paquetes:listar_paquetes')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def editar_paquete(request, pk):
    paquete = get_object_or_404(Paquete, pk=pk)
    
    if request.method == 'POST':
        paquete.nombre = request.POST.get('nombre', paquete.nombre).strip()
        paquete.descripcion = request.POST.get('descripcion', paquete.descripcion).strip()
        paquete.precio_total = request.POST.get('precio_total') or paquete.precio_total
        paquete.estado = request.POST.get('estado', paquete.estado)
        servicio_principal_id = request.POST.get('servicio_principal')
        detalles_json = request.POST.get('detalles_json', '[]')

        paquete.servicio_principal_id = servicio_principal_id or None

        # Eliminar detalles existentes
        paquete.detalles.all().delete()

        # Procesar nuevos detalles
        import json
        try:
            detalles = json.loads(detalles_json)
            for detalle in detalles:
                DetallePaquete.objects.create(
                    paquete=paquete,
                    descripcion=detalle['descripcion'],
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio_unitario']
                )
        except (json.JSONDecodeError, KeyError):
            pass

        paquete.save()
        messages.success(request, 'Paquete actualizado correctamente.')
    return redirect('paquetes:listar_paquetes')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_paquete(request, pk):
    paquete = get_object_or_404(Paquete, pk=pk)
    if request.method == 'POST':
        paquete.delete()
        messages.success(request, 'Paquete eliminado correctamente.')
    return redirect('paquetes:listar_paquetes')
