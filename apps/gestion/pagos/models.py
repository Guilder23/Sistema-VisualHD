from django.db import models
from django.utils import timezone


class Pago(models.Model):
    METODO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('qr', 'QR'),
    ]
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('anulado', 'Anulado'),
    ]

    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.CASCADE, related_name='pagos')
    sesion = models.ForeignKey('sesiones.Sesion', on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Monto (Bs)')
    metodo_pago = models.CharField(max_length=20, choices=METODO_CHOICES, default='efectivo')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_pago = models.DateField(default=timezone.now, verbose_name='Fecha de pago')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f'{self.cliente} - Bs {self.monto}'
