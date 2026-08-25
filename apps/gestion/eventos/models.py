from django.db import models


class Evento(models.Model):
    TIPO_CHOICES = [
        ('boda', 'Boda'),
        ('xv', 'XV Años'),
        ('cumpleaños', 'Cumpleaños'),
        ('corporativo', 'Corporativo'),
        ('otro', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('planificado', 'Planificado'),
        ('confirmado', 'Confirmado'),
        ('en_progreso', 'En progreso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE, related_name='eventos')
    nombre = models.CharField(max_length=255, verbose_name='Nombre del evento')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='otro')
    fecha_inicio = models.DateTimeField(verbose_name='Fecha y hora inicio')
    fecha_fin = models.DateTimeField(verbose_name='Fecha y hora fin')
    ubicacion = models.CharField(max_length=255, verbose_name='Ubicación')
    descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')
    empleados_asignados = models.ManyToManyField('empleados.Empleado', blank=True, related_name='eventos')
    presupuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Presupuesto (Bs)')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='planificado')
    notas = models.TextField(blank=True, default='', verbose_name='Notas internas')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f'{self.nombre} - {self.cliente}'
