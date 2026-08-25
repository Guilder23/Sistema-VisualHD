from django.urls import path
from .views import (
    reportes_inicio,
    reporte_ingresos,
    reporte_egresos,
    reporte_clientes,
    reporte_citas,
    reporte_empleados,
    reporte_financiero,
)

app_name = 'reportes'

urlpatterns = [
    path('', reportes_inicio, name='reportes_inicio'),
    path('ingresos/', reporte_ingresos, name='reporte_ingresos'),
    path('egresos/', reporte_egresos, name='reporte_egresos'),
    path('clientes/', reporte_clientes, name='reporte_clientes'),
    path('citas/', reporte_citas, name='reporte_citas'),
    path('empleados/', reporte_empleados, name='reporte_empleados'),
    path('financiero/', reporte_financiero, name='reporte_financiero'),
]
