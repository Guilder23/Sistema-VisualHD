from django.contrib import admin
from .models import Sesion, AdicionalSesion


class AdicionalSesionInline(admin.TabularInline):
    model = AdicionalSesion
    extra = 0


@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servicio', 'empleado', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'lugar')
    inlines = [AdicionalSesionInline]


@admin.register(AdicionalSesion)
class AdicionalSesionAdmin(admin.ModelAdmin):
    list_display = ('sesion', 'descripcion', 'cantidad', 'precio_unitario')
