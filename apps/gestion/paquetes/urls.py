from django.urls import path
from .views import listar_paquetes, crear_paquete, editar_paquete, eliminar_paquete

app_name = 'paquetes'

urlpatterns = [
    path('', listar_paquetes, name='listar_paquetes'),
    path('crear/', crear_paquete, name='crear_paquete'),
    path('<int:pk>/editar/', editar_paquete, name='editar_paquete'),
    path('<int:pk>/eliminar/', eliminar_paquete, name='eliminar_paquete'),
]
