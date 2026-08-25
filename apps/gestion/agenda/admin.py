from django.contrib import admin
from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha', 'empleado', 'estado', 'duracion_minutos')
    list_filter = ('estado', 'fecha')
    search_fields = ('cliente__nombre', 'cliente__apellido', 'descripcion')
