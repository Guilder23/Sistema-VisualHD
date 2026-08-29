import io
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

MESES = [
    'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
    'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE',
]


def _formatear_fecha(fecha):
    return f'{fecha.day} DE {MESES[fecha.month - 1]} DEL {fecha.year}'


def _ruta_plantilla():
    return Path(settings.BASE_DIR) / 'static' / 'img' / 'plantillaPDF.png'


def _nueva_pagina(c, img, ancho, alto):
    c.showPage()
    if img:
        c.drawImage(img, 0, 0, width=ancho, height=alto, preserveAspectRatio=False, mask='auto')
    return alto - 200


def generar_pdf_cobro(tipo, objeto, pagos, total, pagado, pendiente):
    buffer = io.BytesIO()
    ancho, alto = A4
    c = canvas.Canvas(buffer, pagesize=A4)

    plantilla = _ruta_plantilla()
    img = None
    if plantilla.exists():
        img = ImageReader(str(plantilla))
        c.drawImage(img, 0, 0, width=ancho, height=alto, preserveAspectRatio=False, mask='auto')

    margen_x = 45
    y = alto - 240

    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(ancho / 2, y, 'RESUMEN DE COBRO')
    y -= 35

    cliente = objeto.cliente
    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Cliente:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, str(cliente).upper())
    y -= 18

    hoy = timezone.localdate()
    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Fecha:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, _formatear_fecha(hoy))
    y -= 18

    tipo_label = 'SESIÓN FOTOGRÁFICA' if tipo == 'sesion' else 'EVENTO'
    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Tipo:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, tipo_label)
    y -= 18

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Detalle:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, str(objeto).upper()[:70])
    y -= 18

    if cliente.telefono:
        c.setFont('Helvetica-Bold', 11)
        c.drawString(margen_x, y, 'Teléfono:')
        c.setFont('Helvetica', 11)
        c.drawString(margen_x + 65, y, cliente.telefono)
        y -= 18

    y -= 15
    ancho_tabla = ancho - (margen_x * 2)

    c.setFillColor(colors.HexColor('#333333'))
    c.rect(margen_x, y - 5, ancho_tabla, 22, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(margen_x + 8, y, 'RESUMEN')
    c.setFillColor(colors.black)
    y -= 28

    c.setFont('Helvetica', 10)
    for etiqueta, valor in (
        ('Total:', f'{total:.2f} BS'),
        ('Pagado:', f'{pagado:.2f} BS'),
        ('Pendiente:', f'{pendiente:.2f} BS'),
    ):
        c.drawString(margen_x + 5, y, etiqueta)
        c.drawRightString(ancho - margen_x - 5, y, valor)
        c.setStrokeColor(colors.HexColor('#cccccc'))
        c.line(margen_x, y - 6, ancho - margen_x, y - 6)
        y -= 22

    y -= 15
    c.setFillColor(colors.HexColor('#333333'))
    c.rect(margen_x, y - 5, ancho_tabla, 22, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(margen_x + 8, y, 'FECHA')
    c.drawString(margen_x + 100, y, 'MONTO')
    c.drawString(margen_x + 200, y, 'MÉTODO')
    c.drawRightString(ancho - margen_x - 8, y, 'ESTADO')
    c.setFillColor(colors.black)
    y -= 28

    c.setFont('Helvetica', 10)
    pagos_list = list(pagos)
    if pagos_list:
        for pago in pagos_list:
            if y < 150:
                y = _nueva_pagina(c, img, ancho, alto)
                c.setFont('Helvetica', 10)

            c.drawString(margen_x + 5, y, pago.fecha_pago.strftime('%d/%m/%Y'))
            c.drawString(margen_x + 100, y, f'{pago.monto_pagado:.2f} BS')
            c.drawString(margen_x + 200, y, pago.get_metodo_pago_display().upper())
            c.drawRightString(ancho - margen_x - 5, y, pago.get_estado_display().upper())
            c.setStrokeColor(colors.HexColor('#cccccc'))
            c.line(margen_x, y - 6, ancho - margen_x, y - 6)
            y -= 22
    else:
        c.drawString(margen_x + 5, y, 'SIN PAGOS REGISTRADOS')
        y -= 22

    c.setFont('Helvetica', 8)
    c.setFillColor(colors.HexColor('#666666'))
    estado_cobro = 'COMPLETADO' if pendiente <= 0 else 'PENDIENTE'
    c.drawCentredString(ancho / 2, 130, f'Estado del cobro: {estado_cobro}')

    c.save()
    buffer.seek(0)
    return buffer
