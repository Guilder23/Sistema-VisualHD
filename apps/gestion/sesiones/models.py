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
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total (Bs)')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sesión fotográfica'
        verbose_name_plural = 'Sesiones fotográficas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f'{self.cliente} - {self.fecha}'

    def total_adicionales(self):
        return sum((a.subtotal() for a in self.adicionales.all()), 0)

    def total_general(self):
        total = self.total_adicionales()
        if total:
            return total
        return self.precio


class AdicionalSesion(models.Model):
    sesion = models.ForeignKey(Sesion, on_delete=models.CASCADE, related_name='adicionales')
    descripcion = models.CharField(max_length=200, verbose_name='Descripción del adicional')
    cantidad = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Precio unitario (Bs)')

    class Meta:
        verbose_name = 'Adicional de sesión'
        verbose_name_plural = 'Adicionales de sesión'

    def __str__(self):
        return f'{self.sesion} - {self.descripcion} (x{self.cantidad})'

    def subtotal(self):
        return self.cantidad * self.precio_unitario
