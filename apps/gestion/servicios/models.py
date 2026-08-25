from django.db import models


class Servicio(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=200, verbose_name='Nombre del servicio')
    descripcion = models.TextField(blank=True, default='')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Precio (Bs)')
    duracion_minutos = models.PositiveIntegerField(default=60, verbose_name='Duración estimada (minutos)')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
