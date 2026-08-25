from django.urls import path
from .views import listar_pagos, crear_pago, editar_pago, eliminar_pago

app_name = 'pagos'

urlpatterns = [
    path('', listar_pagos, name='listar_pagos'),
    path('crear/', crear_pago, name='crear_pago'),
    path('<int:pk>/editar/', editar_pago, name='editar_pago'),
    path('<int:pk>/eliminar/', eliminar_pago, name='eliminar_pago'),
]
