from django.db import models


class Sesion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE, related_name='sesiones')
    servicio = models.ForeignKey('servicios.Servicio', on_delete=models.SET_NULL, null=True, blank=True, related_name='sesiones')
    empleado = models.ForeignKey('empleados.Empleado', on_delete=models.SET_NULL, null=True, blank=True, related_name='sesiones', verbose_name='Fotógrafo asignado')
    fecha = models.DateField(verbose_name='Fecha de la sesión')
    hora = models.TimeField(verbose_name='Hora de la sesión')
    lugar = models.CharField(max_length=250, blank=True, default='', verbose_name='Lugar')
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio (Bs)')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sesión fotográfica'
        verbose_name_plural = 'Sesiones fotográficas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f'{self.cliente} - {self.fecha}'
