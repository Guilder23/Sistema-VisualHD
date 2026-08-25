from django.urls import path
from .views import listar_sesiones, crear_sesion, editar_sesion, eliminar_sesion

app_name = 'sesiones'

urlpatterns = [
    path('', listar_sesiones, name='listar_sesiones'),
    path('crear/', crear_sesion, name='crear_sesion'),
    path('<int:pk>/editar/', editar_sesion, name='editar_sesion'),
    path('<int:pk>/eliminar/', eliminar_sesion, name='eliminar_sesion'),
]
