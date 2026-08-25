from django.urls import path
from .views import listar_roles, listar_usuarios, editar_rol_usuario

app_name = 'permisos'

urlpatterns = [
    path('roles/', listar_roles, name='listar_roles'),
    path('usuarios/', listar_usuarios, name='listar_usuarios'),
    path('usuarios/<int:user_id>/editar/', editar_rol_usuario, name='editar_rol_usuario'),
]
