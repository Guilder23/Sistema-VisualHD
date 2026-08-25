from django.urls import path
from .views import listar_empleados, crear_empleado, editar_empleado, eliminar_empleado

app_name = 'empleados'

urlpatterns = [
    path('', listar_empleados, name='listar_empleados'),
    path('crear/', crear_empleado, name='crear_empleado'),
    path('<int:pk>/editar/', editar_empleado, name='editar_empleado'),
    path('<int:pk>/eliminar/', eliminar_empleado, name='eliminar_empleado'),
]
