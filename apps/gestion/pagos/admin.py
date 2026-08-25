from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'sesion', 'monto', 'metodo_pago', 'estado', 'fecha_pago')
    list_filter = ('estado', 'metodo_pago')
    search_fields = ('cliente__nombre', 'cliente__apellido')
