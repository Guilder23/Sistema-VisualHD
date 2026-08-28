from django.contrib import admin
from .models import Evento, AdicionalEvento


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'tipo', 'fecha_inicio', 'estado')
    list_filter = ('tipo', 'estado', 'fecha_inicio')
    search_fields = ('nombre', 'cliente__nombre', 'ubicacion')
    filter_horizontal = ('empleados_asignados',)


@admin.register(AdicionalEvento)
class AdicionalEventoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'descripcion', 'cantidad', 'precio_unitario')
    search_fields = ('descripcion', 'evento__nombre')
