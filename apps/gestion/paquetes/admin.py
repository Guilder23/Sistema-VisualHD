from django.contrib import admin
from .models import Paquete, DetallePaquete


class DetallePaqueteInline(admin.TabularInline):
    model = DetallePaquete
    extra = 0


@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'servicio_principal', 'precio_total', 'estado', 'creado']
    list_filter = ['estado', 'servicio_principal', 'creado']
    search_fields = ['nombre', 'descripcion']
    inlines = [DetallePaqueteInline]


@admin.register(DetallePaquete)
class DetallePaqueteAdmin(admin.ModelAdmin):
    list_display = ['paquete', 'descripcion', 'cantidad', 'precio_unitario']
    list_filter = ['paquete']
