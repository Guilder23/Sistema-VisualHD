from django.urls import path
from .views import listar_servicios, crear_servicio, editar_servicio, eliminar_servicio

app_name = 'servicios'

urlpatterns = [
    path('', listar_servicios, name='listar_servicios'),
    path('crear/', crear_servicio, name='crear_servicio'),
    path('<int:pk>/editar/', editar_servicio, name='editar_servicio'),
    path('<int:pk>/eliminar/', eliminar_servicio, name='eliminar_servicio'),
]
