from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sesiones', '0003_remove_sesion_presupuesto_sesion_precio'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdicionalSesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción del adicional')),
                ('cantidad', models.PositiveIntegerField(default=1, verbose_name='Cantidad')),
                ('precio_unitario', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Precio unitario (Bs)')),
                ('sesion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adicionales', to='sesiones.sesion')),
            ],
            options={
                'verbose_name': 'Adicional de sesión',
                'verbose_name_plural': 'Adicionales de sesión',
            },
        ),
    ]
