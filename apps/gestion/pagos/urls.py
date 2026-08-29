from django.urls import path
from .views import amortizar_pago, crear_pago, editar_pago, eliminar_pago, listar_pagos, pdf_cobro

app_name = 'pagos'

urlpatterns = [
    path('', listar_pagos, name='listar_pagos'),
    path('crear/', crear_pago, name='crear_pago'),
    path('<int:pk>/editar/', editar_pago, name='editar_pago'),
    path('<int:pk>/eliminar/', eliminar_pago, name='eliminar_pago'),
    path('amortizar/', amortizar_pago, name='amortizar_pago'),
    path('pdf/<str:tipo>/<int:objeto_id>/', pdf_cobro, name='pdf_cobro'),
]
