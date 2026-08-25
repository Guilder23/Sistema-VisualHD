from django.db import models


class Cliente(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellido = models.CharField(max_length=150, blank=True, default='', verbose_name='Apellidos')
    email = models.EmailField(blank=True, default='', verbose_name='Correo electrónico')
    telefono = models.CharField(max_length=20, blank=True, default='', verbose_name='Teléfono')
    ci = models.CharField(max_length=30, blank=True, default='', verbose_name='CI / Carnet')
    ciudad = models.CharField(max_length=150, blank=True, default='', verbose_name='Ciudad')
    direccion = models.CharField(max_length=250, blank=True, default='', verbose_name='Dirección')
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-creado']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'.strip()
