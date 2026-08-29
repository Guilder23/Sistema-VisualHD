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

DIAS = [
    'LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO',
]


def _formatear_fecha(fecha):
    return f'{fecha.day} DE {MESES[fecha.month - 1]} DEL {fecha.year}'


def _formatear_fecha_evento(fecha):
    dia = DIAS[fecha.weekday()]
    return f'{dia} {fecha.day} DE {MESES[fecha.month - 1]} {fecha.year}'


def _formatear_hora(fecha):
    return fecha.strftime('%H:%M')


def _ruta_plantilla():
    return Path(settings.BASE_DIR) / 'static' / 'img' / 'plantillaPDF.png'


def generar_pdf_evento(evento):
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

    titulo = 'COTIZACIÓN EVENTO'
    if evento.servicio:
        titulo = f'COTIZACIÓN {evento.servicio.nombre.upper()}'

    c.setFont('Helvetica-Bold', 16)
    c.drawCentredString(ancho / 2, y, titulo)
    y -= 35

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Cliente:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, str(evento.cliente).upper())
    y -= 18

    hoy = timezone.localdate()
    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Fecha:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, _formatear_fecha(hoy))
    y -= 18

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Evento:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, evento.nombre.upper())
    y -= 18

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Tipo:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, evento.get_tipo_display().upper())
    y -= 18

    fecha_inicio = timezone.localtime(evento.fecha_inicio)
    fecha_fin = timezone.localtime(evento.fecha_fin)

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Inicio:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, f'{_formatear_fecha_evento(fecha_inicio.date())} {_formatear_hora(fecha_inicio)}')
    y -= 18

    c.setFont('Helvetica-Bold', 11)
    c.drawString(margen_x, y, 'Fin:')
    c.setFont('Helvetica', 11)
    c.drawString(margen_x + 55, y, f'{_formatear_fecha_evento(fecha_fin.date())} {_formatear_hora(fecha_fin)}')
    y -= 18

    if evento.ubicacion:
        c.setFont('Helvetica-Bold', 11)
        c.drawString(margen_x, y, 'Ubicación:')
        c.setFont('Helvetica', 11)
        c.drawString(margen_x + 70, y, evento.ubicacion.upper())
        y -= 18

    empleados = list(evento.empleados_asignados.all())
    if empleados:
        c.setFont('Helvetica-Bold', 11)
        c.drawString(margen_x, y, 'Equipo:')
        c.setFont('Helvetica', 11)
        nombres = ', '.join(str(e).upper() for e in empleados)
        c.drawString(margen_x + 55, y, nombres[:80])
        y -= 18

    if evento.cliente.telefono:
        c.setFont('Helvetica-Bold', 11)
        c.drawString(margen_x, y, 'Teléfono:')
        c.setFont('Helvetica', 11)
        c.drawString(margen_x + 65, y, evento.cliente.telefono)
        y -= 18

    y -= 15
    col_servicio = margen_x
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
    total = Decimal('0')

    if evento.paquete:
        precio_paquete = evento.paquete.precio_total or Decimal('0')
        total += precio_paquete
        descripcion = f'PAQUETE: {evento.paquete.nombre.upper()}'
        c.drawString(col_servicio + 5, y, descripcion[:90])
        c.drawRightString(ancho - margen_x - 5, y, f'{precio_paquete:.2f} BS')
        c.setStrokeColor(colors.HexColor('#cccccc'))
        c.line(col_servicio, y - 6, ancho - margen_x, y - 6)
        y -= 22

    adicionales = list(evento.adicionales.all())
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

    if not evento.paquete and not adicionales:
        c.drawString(col_servicio + 5, y, 'SIN ÍTEMS REGISTRADOS')
        c.drawRightString(ancho - margen_x - 5, y, '0.00 BS')
        y -= 22

    if not total:
        total = evento.total_general()

    y -= 10
    c.setFont('Helvetica-Bold', 11)
    c.drawRightString(ancho - margen_x - 90, y, 'Total:')
    c.drawRightString(ancho - margen_x - 5, y, f'{total:.2f} BS')

    nota = evento.notas or evento.descripcion
    if nota:
        y -= 35
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(ancho / 2, y, f'NOTA: {nota.upper()}')

    c.setFont('Helvetica', 8)
    c.setFillColor(colors.HexColor('#666666'))
    c.drawCentredString(ancho / 2, 130, f'Estado: {evento.get_estado_display().upper()}')

    c.save()
    buffer.seek(0)
    return buffer
