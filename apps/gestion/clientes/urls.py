from django.urls import path
from .views import listar_clientes, crear_cliente, editar_cliente, eliminar_cliente

app_name = 'clientes'

urlpatterns = [
    path('', listar_clientes, name='listar_clientes'),
    path('crear/', crear_cliente, name='crear_cliente'),
    path('<int:pk>/editar/', editar_cliente, name='editar_cliente'),
    path('<int:pk>/eliminar/', eliminar_cliente, name='eliminar_cliente'),
]
