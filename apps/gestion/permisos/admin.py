from django.contrib import admin
from .models import Rol, RolUsuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)
    fieldsets = (
        ('Información básica', {'fields': ('nombre', 'descripcion')}),
        ('Permisos de módulos', {
            'fields': (
                'puede_ver_dashboard',
                'puede_gestionar_clientes',
                'puede_gestionar_servicios',
                'puede_gestionar_sesiones',
                'puede_gestionar_empleados',
                'puede_gestionar_pagos',
                'puede_gestionar_agenda',
                'puede_gestionar_eventos',
                'puede_ver_finanzas',
                'puede_ver_reportes',
                'puede_gestionar_usuarios',
                'puede_gestionar_roles',
            )
        }),
    )


@admin.register(RolUsuario)
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'asignado_el')
    list_filter = ('rol',)
    search_fields = ('usuario__username',)
