from django.db import models


class Empleado(models.Model):
    CARGO_CHOICES = [
        ('fotografo', 'Fotógrafo'),
        ('editor', 'Editor'),
        ('asistente', 'Asistente'),
        ('administrativo', 'Administrativo'),
    ]
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellido = models.CharField(max_length=150, blank=True, default='', verbose_name='Apellidos')
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='fotografo')
    telefono = models.CharField(max_length=20, blank=True, default='', verbose_name='Teléfono')
    email = models.EmailField(blank=True, default='', verbose_name='Correo electrónico')
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de ingreso')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    observacion = models.TextField(blank=True, default='', verbose_name='Observación')

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'.strip()
