from django.db import models
from django.utils import timezone


class Cita(models.Model):
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('reprogramada', 'Reprogramada'),
    ]

    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE, related_name='citas')
    sesion = models.OneToOneField('sesiones.Sesion', on_delete=models.SET_NULL, null=True, blank=True, related_name='cita')
    empleado = models.ForeignKey('empleados.Empleado', on_delete=models.SET_NULL, null=True, blank=True, related_name='citas')
    fecha = models.DateTimeField(verbose_name='Fecha y hora')
    duracion_minutos = models.IntegerField(default=60, verbose_name='Duración (minutos)')
    descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programada')
    ubicacion = models.CharField(max_length=255, blank=True, default='', verbose_name='Ubicación/Estudio')
    notas = models.TextField(blank=True, default='', verbose_name='Notas internas')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.cliente} - {self.fecha.strftime("%d/%m/%Y %H:%M")}'
