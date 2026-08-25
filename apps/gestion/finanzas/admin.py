from django.contrib import admin
from .models import Ingreso, Egreso, Caja, PagoEmpleado, ServicioBasico


@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('concepto', 'categoria', 'monto', 'fecha', 'cliente')
    list_filter = ('categoria', 'fecha')
    search_fields = ('concepto', 'cliente__nombre')


@admin.register(Egreso)
class EgresoAdmin(admin.ModelAdmin):
    list_display = ('concepto', 'categoria', 'monto', 'fecha')
    list_filter = ('categoria', 'fecha')
    search_fields = ('concepto', 'comprobante')


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'saldo_inicial', 'total_ingresos', 'total_egresos', 'saldo_final')
    list_filter = ('fecha',)
    readonly_fields = ('creado', 'actualizado')


@admin.register(PagoEmpleado)
class PagoEmpleadoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'mes_año', 'total_a_pagar', 'monto_pagado', 'estado')
    list_filter = ('estado', 'mes_año', 'empleado')
    search_fields = ('empleado__nombre', 'mes_año')


@admin.register(ServicioBasico)
class ServicioBasicoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'mes_año', 'monto', 'fecha_pago')
    list_filter = ('tipo', 'mes_año')
    search_fields = ('referencia_pago',)
