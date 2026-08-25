from django.contrib import admin
from .models import Empleado


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cargo', 'telefono', 'estado')
    list_filter = ('estado', 'cargo')
    search_fields = ('nombre', 'apellido', 'email')
