from django.db import models


class Paquete(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    servicio_principal = models.ForeignKey('servicios.Servicio', on_delete=models.SET_NULL, null=True, blank=True, related_name='paquetes', verbose_name='Servicio principal')
    nombre = models.CharField(max_length=200, verbose_name='Nombre del paquete')
    descripcion = models.TextField(blank=True, default='', verbose_name='Descripción')
    precio_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Precio total (Bs)')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Paquete'
        verbose_name_plural = 'Paquetes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def actualizar_precio_total(self):
        """Actualiza el precio total basado en los detalles del paquete"""
        total = sum(detalle.cantidad * detalle.precio_unitario for detalle in self.detalles.all())
        self.precio_total = total
        self.save()


class DetallePaquete(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='detalles')
    descripcion = models.CharField(max_length=200, verbose_name='Descripción del item')
    cantidad = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Precio unitario (Bs)')

    class Meta:
        verbose_name = 'Detalle de paquete'
        verbose_name_plural = 'Detalles de paquetes'

    def __str__(self):
        return f'{self.paquete} - {self.descripcion} (x{self.cantidad})'

    def subtotal(self):
        return self.cantidad * self.precio_unitario
