from django.db import models
from django.contrib.auth.models import User


class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre del rol')
    descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')
    
    # Permisos específicos de módulos
    puede_ver_dashboard = models.BooleanField(default=False)
    puede_gestionar_clientes = models.BooleanField(default=False)
    puede_gestionar_servicios = models.BooleanField(default=False)
    puede_gestionar_sesiones = models.BooleanField(default=False)
    puede_gestionar_empleados = models.BooleanField(default=False)
    puede_gestionar_pagos = models.BooleanField(default=False)
    puede_gestionar_agenda = models.BooleanField(default=False)
    puede_gestionar_eventos = models.BooleanField(default=False)
    puede_ver_finanzas = models.BooleanField(default=False)
    puede_ver_reportes = models.BooleanField(default=False)
    puede_gestionar_usuarios = models.BooleanField(default=False)
    puede_gestionar_roles = models.BooleanField(default=False)
    
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class RolUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rol_usuario')
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    asignado_el = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rol de usuario'
        verbose_name_plural = 'Roles de usuarios'

    def __str__(self):
        return f'{self.usuario.username} - {self.rol}'
