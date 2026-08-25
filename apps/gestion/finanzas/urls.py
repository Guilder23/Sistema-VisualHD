from django.urls import path
from .views import crear_egreso, editar_egreso, eliminar_egreso, finanzas_dashboard

app_name = 'finanzas'

urlpatterns = [
    path('', finanzas_dashboard, name='finanzas_dashboard'),
    path('egresos/crear/', crear_egreso, name='crear_egreso'),
    path('egresos/<int:pk>/editar/', editar_egreso, name='editar_egreso'),
    path('egresos/<int:pk>/eliminar/', eliminar_egreso, name='eliminar_egreso'),
]
