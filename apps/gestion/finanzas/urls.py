from django.urls import path
from .views import amortizar_pago_empleado, anular_pago_empleado, crear_egreso, crear_pago_empleado, editar_egreso, editar_pago_empleado, eliminar_egreso, finanzas_dashboard, listar_pagos_empleados

app_name = 'finanzas'

urlpatterns = [
    path('', finanzas_dashboard, name='finanzas_dashboard'),
    path('egresos/crear/', crear_egreso, name='crear_egreso'),
    path('egresos/<int:pk>/editar/', editar_egreso, name='editar_egreso'),
    path('egresos/<int:pk>/eliminar/', eliminar_egreso, name='eliminar_egreso'),
    path('pagos-empleados/', listar_pagos_empleados, name='listar_pagos_empleados'),
    path('pagos-empleados/crear/', crear_pago_empleado, name='crear_pago_empleado'),
    path('pagos-empleados/<int:pk>/editar/', editar_pago_empleado, name='editar_pago_empleado'),
    path('pagos-empleados/<int:pk>/anular/', anular_pago_empleado, name='anular_pago_empleado'),
    path('pagos-empleados/<int:pk>/amortizar/', amortizar_pago_empleado, name='amortizar_pago_empleado'),
]
