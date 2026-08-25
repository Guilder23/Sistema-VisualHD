from django.urls import path
from .views import listar_citas, crear_cita, editar_cita, eliminar_cita

app_name = 'agenda'

urlpatterns = [
    path('', listar_citas, name='listar_citas'),
    path('crear/', crear_cita, name='crear_cita'),
    path('<int:pk>/editar/', editar_cita, name='editar_cita'),
    path('<int:pk>/eliminar/', eliminar_cita, name='eliminar_cita'),
]
