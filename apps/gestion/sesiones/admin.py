from django.contrib import admin
from .models import Sesion


@admin.register(Sesion)
class SesionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servicio', 'empleado', 'fecha', 'hora', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'lugar')
