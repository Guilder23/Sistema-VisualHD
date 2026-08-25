from django.db import models
from django.utils import timezone


class Ingreso(models.Model):
    CATEGORIA_CHOICES = [
        ('sesion_foto', 'Sesión fotográfica'),
        ('evento', 'Evento'),
        ('servicio', 'Servicio'),
        ('paquete', 'Paquete'),
        ('otro', 'Otro'),
    ]

    cliente = models.ForeignKey('clientes.Cliente', on_delete=models.SET_NULL, null=True, blank=True, related_name='ingresos')
    pago = models.OneToOneField('pagos.Pago', on_delete=models.SET_NULL, null=True, blank=True, related_name='ingreso_financiero')
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='sesion_foto')
    concepto = models.CharField(max_length=255, verbose_name='Concepto/Descripción')
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto (Bs)')
    fecha = models.DateField(default=timezone.now)
    referencia = models.CharField(max_length=100, blank=True, default='', verbose_name='Referencia (recibo, etc)')
    notas = models.TextField(blank=True, default='')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.concepto} - Bs. {self.monto}'


class Egreso(models.Model):
    CATEGORIA_CHOICES = [
        ('wifi', 'WiFi / Internet'),
        ('agua', 'Agua'),
        ('luz', 'Luz / Electricidad'),
        ('gas', 'Gas'),
        ('tienda', 'Gastos de la tienda'),
        ('estudio', 'Gastos del foto estudio'),
        ('materiales', 'Materiales de fotografía'),
        ('transporte', 'Transporte'),
        ('marketing', 'Marketing/publicidad'),
        ('otro', 'Otro'),
    ]

    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default='otro')
    concepto = models.CharField(max_length=255, verbose_name='Concepto/Descripción')
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto (Bs)')
    fecha = models.DateField(default=timezone.now)
    comprobante = models.CharField(max_length=100, blank=True, default='', verbose_name='Comprobante/Factura')
    notas = models.TextField(blank=True, default='')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Egreso'
        verbose_name_plural = 'Egresos'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.concepto} - Bs. {self.monto}'


class Caja(models.Model):
    fecha = models.DateField(default=timezone.now, unique=True, verbose_name='Fecha')
    saldo_inicial = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Saldo inicial (Bs)')
    total_ingresos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_egresos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_final = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Saldo final (Bs)')
    notas = models.TextField(blank=True, default='', verbose_name='Notas de cierre')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'
        ordering = ['-fecha']

    def __str__(self):
        return f'Caja {self.fecha.strftime("%d/%m/%Y")}'


class PagoEmpleado(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('parcial', 'Parcial'),
    ]

    empleado = models.ForeignKey('empleados.Empleado', on_delete=models.CASCADE, related_name='pagos')
    mes_año = models.CharField(max_length=10, verbose_name='Mes/Año (MM/YYYY)')
    monto_base = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto base (Bs)')
    bonificación = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Bonificación (Bs)')
    descuentos = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Descuentos (Bs)')
    total_a_pagar = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total a pagar (Bs)')
    monto_pagado = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Monto pagado (Bs)')
    fecha_pago = models.DateField(null=True, blank=True, verbose_name='Fecha de pago')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    comprobante = models.CharField(max_length=100, blank=True, default='', verbose_name='Comprobante/Transferencia')
    notas = models.TextField(blank=True, default='')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pago de empleado'
        verbose_name_plural = 'Pagos de empleados'
        unique_together = ('empleado', 'mes_año')
        ordering = ['-mes_año']

    def __str__(self):
        return f'{self.empleado} - {self.mes_año}'


class ServicioBasico(models.Model):
    TIPO_CHOICES = [
        ('agua', 'Agua'),
        ('electricidad', 'Electricidad'),
        ('gas', 'Gas'),
        ('internet', 'Internet'),
        ('telefono', 'Teléfono'),
        ('otro', 'Otro'),
    ]

    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='otro')
    mes_año = models.CharField(max_length=10, verbose_name='Mes/Año (MM/YYYY)')
    monto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto (Bs)')
    referencia_pago = models.CharField(max_length=100, blank=True, default='', verbose_name='Referencia de pago')
    fecha_pago = models.DateField(default=timezone.now)
    notas = models.TextField(blank=True, default='')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Servicio básico'
        verbose_name_plural = 'Servicios básicos'
        unique_together = ('tipo', 'mes_año')
        ordering = ['-mes_año']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.mes_año}'
