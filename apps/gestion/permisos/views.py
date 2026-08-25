from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

from .models import Rol, RolUsuario


def puede_gestionar(usuario, permiso):
    if not usuario.is_staff:
        return False
    asignacion = RolUsuario.objects.select_related('rol').filter(usuario=usuario).first()
    if not asignacion or not asignacion.rol:
        return True
    return bool(asignacion and asignacion.rol and getattr(asignacion.rol, permiso, False))


@login_required
@user_passes_test(lambda u: puede_gestionar(u, 'puede_gestionar_roles'), login_url='/login/')
def listar_roles(request):
    roles = Rol.objects.all()
    return render(request, 'gestion/permisos/roles.html', {
        'roles': roles,
    })


@login_required
@user_passes_test(lambda u: puede_gestionar(u, 'puede_gestionar_usuarios'), login_url='/login/')
def listar_usuarios(request):
    usuarios = User.objects.filter(is_staff=True).select_related('rol_usuario__rol')
    return render(request, 'gestion/permisos/usuarios.html', {
        'usuarios': usuarios,
    })


@login_required
@user_passes_test(lambda u: puede_gestionar(u, 'puede_gestionar_usuarios'), login_url='/login/')
def editar_rol_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id, is_staff=True)
    if request.method == 'POST':
        rol_id = request.POST.get('rol_id')
        rol = Rol.objects.filter(id=rol_id).first()
        
        rol_usuario, _ = RolUsuario.objects.get_or_create(usuario=usuario)
        rol_usuario.rol = rol
        rol_usuario.save()
    
    return redirect('permisos:listar_usuarios')
