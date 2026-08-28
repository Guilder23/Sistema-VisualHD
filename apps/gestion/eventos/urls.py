from django.urls import path
from .views import (
    listar_eventos, crear_evento, editar_evento, eliminar_evento,
    obtener_paquetes_por_servicio, obtener_detalle_paquete, obtener_eventos_calendario
)

app_name = 'eventos'

urlpatterns = [
    path('', listar_eventos, name='listar_eventos'),
    path('crear/', crear_evento, name='crear_evento'),
    path('<int:pk>/editar/', editar_evento, name='editar_evento'),
    path('<int:pk>/eliminar/', eliminar_evento, name='eliminar_evento'),
    path('api/paquetes-por-servicio/', obtener_paquetes_por_servicio, name='api_paquetes_por_servicio'),
    path('api/detalle-paquete/', obtener_detalle_paquete, name='api_detalle_paquete'),
    path('api/calendario/', obtener_eventos_calendario, name='api_calendario'),
]
