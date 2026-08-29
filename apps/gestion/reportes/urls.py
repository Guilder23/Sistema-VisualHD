from django.urls import path
from .views import (
    reportes_inicio,
    reporte_ingresos, pdf_ingresos,
    reporte_egresos, pdf_egresos,
    reporte_clientes, pdf_clientes,
    reporte_citas, pdf_citas,
    reporte_empleados, pdf_empleados,
    reporte_financiero, pdf_financiero,
)

app_name = 'reportes'

urlpatterns = [
    path('', reportes_inicio, name='reportes_inicio'),
    path('ingresos/', reporte_ingresos, name='reporte_ingresos'),
    path('ingresos/pdf/', pdf_ingresos, name='pdf_ingresos'),
    path('egresos/', reporte_egresos, name='reporte_egresos'),
    path('egresos/pdf/', pdf_egresos, name='pdf_egresos'),
    path('clientes/', reporte_clientes, name='reporte_clientes'),
    path('clientes/pdf/', pdf_clientes, name='pdf_clientes'),
    path('citas/', reporte_citas, name='reporte_citas'),
    path('citas/pdf/', pdf_citas, name='pdf_citas'),
    path('empleados/', reporte_empleados, name='reporte_empleados'),
    path('empleados/pdf/', pdf_empleados, name='pdf_empleados'),
    path('financiero/', reporte_financiero, name='reporte_financiero'),
    path('financiero/pdf/', pdf_financiero, name='pdf_financiero'),
]
