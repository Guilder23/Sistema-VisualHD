from datetime import date, time
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase

from apps.gestion.clientes.models import Cliente
from apps.gestion.empleados.models import Empleado
from apps.gestion.eventos.models import Evento
from apps.gestion.finanzas.models import PagoEmpleado
from apps.gestion.finanzas.views import amortizar_pago_empleado
from apps.gestion.pagos.models import Pago
from apps.gestion.pagos.views import amortizar_pago
from apps.gestion.sesiones.models import Sesion


class AmortizacionDecimalTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='secret123',
            is_staff=True,
        )
        self.cliente = Cliente.objects.create(
            nombre='Ana',
            apellido='García',
            email='ana@example.com',
            telefono='76543210',
        )
        self.empleado = Empleado.objects.create(
            nombre='Luis',
            apellido='Mamani',
            cargo='fotografo',
            telefono='71234567',
            email='luis@example.com',
        )

    def test_amortizar_pago_sesion_acepta_valores_decimal(self):
        sesion = Sesion.objects.create(
            cliente=self.cliente,
            fecha=date(2026, 8, 26),
            hora=time(15, 30),
            precio=Decimal('500.00'),
        )
        pago = Pago.objects.create(
            cliente=self.cliente,
            sesion=sesion,
            monto=Decimal('500.00'),
            monto_pagado=Decimal('200.00'),
            metodo_pago='efectivo',
            fecha_pago=date(2026, 8, 26),
            estado='parcial',
        )

        request = self.factory.post(
            '/gestion/pagos/amortizar/',
            {
                'tipo': 'sesion',
                'objeto_id': str(sesion.pk),
                'monto_amortizar': '150.25',
                'metodo_pago': 'efectivo',
                'fecha_amortizacion': '2026-08-26',
                'observacion': 'Abono',
            },
        )
        SessionMiddleware(lambda req: None).process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)
        request.user = self.user

        response = amortizar_pago(request)

        self.assertEqual(response.status_code, 302)
        pago.refresh_from_db()
        self.assertEqual(pago.monto_pagado, Decimal('350.25'))
        self.assertEqual(pago.estado, 'parcial')

    def test_amortizar_pago_empleado_no_mezcla_decimal_y_float(self):
        pago = PagoEmpleado.objects.create(
            empleado=self.empleado,
            mes_año='08/2026',
            monto_base=Decimal('1000.00'),
            bonificación=Decimal('0.00'),
            descuentos=Decimal('0.00'),
            total_a_pagar=Decimal('1000.00'),
            monto_pagado=Decimal('200.00'),
            fecha_pago=date(2026, 8, 1),
            estado='parcial',
        )

        request = self.factory.post(
            '/gestion/finanzas/pagos-empleados/1/amortizar/',
            {
                'monto_amortizar': '250.50',
                'fecha_amortizacion': '2026-08-26',
            },
        )
        SessionMiddleware(lambda req: None).process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)
        request.user = self.user

        response = amortizar_pago_empleado(request, pago.pk)

        self.assertEqual(response.status_code, 302)
        pago.refresh_from_db()
        self.assertEqual(pago.monto_pagado, Decimal('450.50'))
        self.assertEqual(pago.estado, 'parcial')
