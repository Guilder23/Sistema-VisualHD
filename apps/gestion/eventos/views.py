from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import json

from .models import Evento, AdicionalEvento
from apps.gestion.clientes.models import Cliente
from apps.gestion.empleados.models import Empleado
from apps.gestion.servicios.models import Servicio
from apps.gestion.paquetes.models import Paquete


def _guardar_adicionales(evento, adicionales_json):
    evento.adicionales.all().delete()
    try:
        adicionales = json.loads(adicionales_json or '[]')
        for item in adicionales:
            AdicionalEvento.objects.create(
                evento=evento,
                descripcion=item['descripcion'],
                cantidad=item['cantidad'],
                precio_unitario=item['precio_unitario']
            )
    except (json.JSONDecodeError, KeyError, TypeError):
        pass


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def listar_eventos(request):
    q = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    estado = request.GET.get('estado', '').strip()
    servicio_id = request.GET.get('servicio_id', '').strip()
    paquete_id = request.GET.get('paquete_id', '').strip()
    orden = request.GET.get('orden', 'fecha_desc').strip()

    eventos = Evento.objects.select_related('cliente', 'servicio', 'paquete', 'paquete__servicio_principal').prefetch_related('empleados_asignados', 'adicionales').all()
    if q:
        eventos = eventos.filter(Q(nombre__icontains=q) | Q(cliente__nombre__icontains=q))
    if tipo:
        eventos = eventos.filter(tipo=tipo)
    if estado:
        eventos = eventos.filter(estado=estado)
    if servicio_id:
        eventos = eventos.filter(servicio_id=servicio_id)
    if paquete_id:
        eventos = eventos.filter(paquete_id=paquete_id)

    eventos = eventos.order_by('fecha_inicio' if orden == 'fecha_asc' else '-fecha_inicio')

    paginator = Paginator(eventos, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    qs_sin_page = request.GET.copy()
    qs_sin_page.pop('page', None)

    paquetes_qs = Paquete.objects.filter(estado='activo').select_related('servicio_principal').order_by('nombre')
    paquetes_serializados = []
    for p in paquetes_qs:
        paquetes_serializados.append({
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion or '',
            'precio_total': float(p.precio_total) if p.precio_total is not None else 0.0,
            'servicio_principal_id': p.servicio_principal_id
        })
    paquetes_json = json.dumps(paquetes_serializados, ensure_ascii=False)

    return render(request, 'gestion/eventos/eventos.html', {
        'page_obj': page_obj,
        'q': q,
        'tipo': tipo,
        'estado': estado,
        'servicio_id': servicio_id,
        'paquete_id': paquete_id,
        'orden': orden,
        'querystring': qs_sin_page.urlencode(),
        'clientes': Cliente.objects.filter(estado='activo'),
        'empleados': Empleado.objects.filter(estado='activo'),
        'servicios': Servicio.objects.filter(estado='activo').order_by('nombre'),
        'paquetes': paquetes_qs,
        'paquetes_json': paquetes_json,
    })


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def crear_evento(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente_id')
        nombre = request.POST.get('nombre', '').strip()
        tipo = request.POST.get('tipo', 'otro')
        servicio_id = request.POST.get('servicio_id')
        paquete_id = request.POST.get('paquete_id')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ubicacion = request.POST.get('ubicacion', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        notas = request.POST.get('notas', '').strip()
        adicionales_json = request.POST.get('adicionales_json', '[]')

        cliente = Cliente.objects.filter(id=cliente_id).first()
        if not cliente:
            return redirect('eventos:listar_eventos')

        servicio = Servicio.objects.filter(id=servicio_id).first() if servicio_id else None
        paquete = Paquete.objects.filter(id=paquete_id).first() if paquete_id else None

        evento = Evento.objects.create(
            cliente=cliente,
            nombre=nombre,
            tipo=tipo,
            servicio=servicio,
            paquete=paquete,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            ubicacion=ubicacion,
            descripcion=descripcion,
            notas=notas,
        )
        _guardar_adicionales(evento, adicionales_json)
        evento.presupuesto = evento.total_general()
        evento.save(update_fields=['presupuesto'])
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
        servicio_id = request.POST.get('servicio_id')
        evento.servicio = Servicio.objects.filter(id=servicio_id).first() if servicio_id else None
        paquete_id = request.POST.get('paquete_id')
        evento.paquete = Paquete.objects.filter(id=paquete_id).first() if paquete_id else None
        evento.fecha_inicio = request.POST.get('fecha_inicio') or evento.fecha_inicio
        evento.fecha_fin = request.POST.get('fecha_fin') or evento.fecha_fin
        evento.ubicacion = request.POST.get('ubicacion', evento.ubicacion).strip()
        evento.descripcion = request.POST.get('descripcion', evento.descripcion).strip()
        evento.estado = request.POST.get('estado', evento.estado)
        evento.notas = request.POST.get('notas', evento.notas).strip()
        evento.save()
        _guardar_adicionales(evento, request.POST.get('adicionales_json', '[]'))
        evento.presupuesto = evento.total_general()
        evento.save(update_fields=['presupuesto'])
    return redirect('eventos:listar_eventos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.delete()
    return redirect('eventos:listar_eventos')


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def obtener_paquetes_por_servicio(request):
    servicio_id = request.GET.get('servicio_id')
    if not servicio_id:
        return JsonResponse({'paquetes': []})
    
    paquetes = Paquete.objects.filter(
        servicio_principal_id=servicio_id,
        estado='activo'
    ).select_related('servicio_principal')

    paquetes_list = []
    for p in paquetes:
        paquetes_list.append({
            'id': p.id,
            'nombre': p.nombre,
            'descripcion': p.descripcion,
            'precio_total': float(p.precio_total),
            'servicio_principal__nombre': p.servicio_principal.nombre if p.servicio_principal else ''
        })

    return JsonResponse({'paquetes': paquetes_list})


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def obtener_detalle_paquete(request):
    paquete_id = request.GET.get('paquete_id')
    if not paquete_id:
        return JsonResponse({'detalles': []})
    
    paquete = Paquete.objects.filter(id=paquete_id).prefetch_related('detalles').first()
    if not paquete:
        return JsonResponse({'detalles': []})
    
    detalles = []
    for detalle in paquete.detalles.all():
        detalles.append({
            'descripcion': detalle.descripcion,
            'cantidad': detalle.cantidad,
            'precio_unitario': float(detalle.precio_unitario),
            'subtotal': float(detalle.subtotal())
        })
    
    return JsonResponse({
        'detalles': detalles,
        'precio_total': float(paquete.precio_total),
        'nombre': paquete.nombre
    })


ESTADO_COLORES = {
    'planificado': '#64748B',
    'confirmado': '#059669',
    'en_progreso': '#C81D31',
    'completado': '#0284C7',
    'cancelado': '#DC2626',
}


@login_required
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def obtener_eventos_calendario(request):
    eventos = Evento.objects.select_related('cliente', 'servicio', 'paquete').all()
    data = []
    for evento in eventos:
        data.append({
            'id': evento.id,
            'title': evento.nombre,
            'start': evento.fecha_inicio.isoformat(),
            'end': evento.fecha_fin.isoformat(),
            'color': ESTADO_COLORES.get(evento.estado, '#64748B'),
            'extendedProps': {
                'cliente': f'{evento.cliente.nombre} {evento.cliente.apellido}',
                'servicio': evento.servicio.nombre if evento.servicio else '-',
                'estado': evento.get_estado_display(),
                'ubicacion': evento.ubicacion,
            }
        })
    return JsonResponse({'eventos': data})
