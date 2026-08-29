import io
from decimal import Decimal
from pathlib import Path

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

MESES = [
    'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO',
    'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE',
]

DIAS = [
    'LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO',
]


def _formatear_fecha(fecha):
    return f'{fecha.day} DE {MESES[fecha.month - 1]} DEL {fecha.year}'


def _formatear_fecha_sesion(fecha):
    dia = DIAS[fecha.weekday()]
    return f'{dia} {fecha.day} DE {MESES[fecha.month - 1]} {fecha.year}'


def _ruta_plantilla():
    return Path(settings.BASE_DIR) / 'static' / 'img' / 'plantillaPDF.png'


def generar_pdf_sesion(sesion):
    buffer = io.BytesIO()
    ancho, alto = A4
    c = canvas.Canvas(buffer, pagesize=A4)

    plantilla = _ruta_plantilla()
    img = None
    if plantilla.exists():
        img = ImageReader(str(plantilla))
        c.drawImage(img, 0, 0, width=ancho, height=alto, preserveAspectRatio=False, mask='auto')

    margen_x = 45
    inicio_contenido = alto - 240
    y = inicio_contenido

    titulo = 'COTIZACIÓN SESIÓN FOTOGRÁFICA'
    if sesion.servicio:
        titulo = f'COTIZACIÓN {sesion.servicio.nombre.upper()}'

    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(ancho / 2, y, titulo)
    y -= 35

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Cliente:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, str(sesion.cliente).upper())
    y -= 18

    from django.utils import timezone
    hoy = timezone.localdate()

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Fecha:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, _formatear_fecha(hoy))
    y -= 18

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Para:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, _formatear_fecha_sesion(sesion.fecha))
    y -= 18

    if sesion.hora:
        c.setFont('Helvetica-Bold', 11)
        c.drawString(margen_x, y, 'Hora:')
        c.setFont('Helvetica', 11)
        c.drawString(margen_x + 55, y, sesion.hora.strftime('%H:%M'))
        y -= 18

    if sesion.lugar:
        c.setFont('Helvetica-Bold', 11)
        c.drawString(margen_x, y, 'Lugar:')
        c.setFont('Helvetica', 11)
        c.drawString(margen_x + 55, y, sesion.lugar.upper())
        y -= 18

    if sesion.empleado:
        c.setFont('Helvetica-Bold', 11)
        c.drawString(margen_x, y, 'Fotógrafo:')
        c.setFont('Helvetica', 11)
        c.drawString(margen_x + 70, y, str(sesion.empleado).upper())
        y -= 18

    if sesion.cliente.telefono:
        c.setFont('Helvetica-Bold', 11)
        c.drawString(margen_x, y, 'Teléfono:')
        c.setFont('Helvetica', 11)
        c.drawString(margen_x + 65, y, sesion.cliente.telefono)
        y -= 18

    y -= 15
    col_servicio = margen_x
    col_precio = ancho - margen_x - 80
    ancho_tabla = ancho - (margen_x * 2)

    c.setFillColor(colors.HexColor('#333333'))
    c.rect(col_servicio, y - 5, ancho_tabla, 22, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(col_servicio + 8, y, 'SERVICIO PROFESIONAL')
    c.drawRightString(ancho - margen_x - 8, y, 'PRECIO')
    c.setFillColor(colors.black)
    y -= 28

    c.setFont('Helvetica', 10)
    adicionales = list(sesion.adicionales.all())
    total = Decimal('0')

    for item in adicionales:
        subtotal = item.subtotal()
        total += subtotal
        descripcion = item.descripcion.upper()
        if item.cantidad > 1:
            descripcion = f'{descripcion} (x{item.cantidad})'

        if y < 200:
            c.showPage()
            if img:
                c.drawImage(img, 0, 0, width=ancho, height=alto, preserveAspectRatio=False, mask='auto')
            y = alto - 200
            c.setFont('Helvetica', 10)

        c.drawString(col_servicio + 5, y, descripcion[:90])
        c.drawRightString(ancho - margen_x - 5, y, f'{subtotal:.2f} BS')
        c.setStrokeColor(colors.HexColor('#cccccc'))
        c.line(col_servicio, y - 6, ancho - margen_x, y - 6)
        y -= 22

    if not adicionales:
        c.drawString(col_servicio + 5, y, 'SIN ÍTEMS REGISTRADOS')
        c.drawRightString(ancho - margen_x - 5, y, '0.00 BS')
        y -= 22

    if not total:
        total = sesion.total_general()

    y -= 10
    c.setFont('Helvetica-Bold', 11)
    c.drawRightString(ancho - margen_x - 90, y, 'Total:')
    c.drawRightString(ancho - margen_x - 5, y, f'{total:.2f} BS')

    if sesion.observacion:
        y -= 35
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(ancho / 2, y, f'NOTA: {sesion.observacion.upper()}')

    c.setFont('Helvetica', 8)
    c.setFillColor(colors.HexColor('#666666'))
    c.drawCentredString(ancho / 2, 130, f'Estado: {sesion.get_estado_display().upper()}')

    c.save()
    buffer.seek(0)
    return buffer
