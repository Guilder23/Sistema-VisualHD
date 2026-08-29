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


def _ruta_plantilla():
    return Path(settings.BASE_DIR) / 'static' / 'img' / 'plantillaPDF.png'


def _formatear_fecha(fecha):
    if not fecha:
        return '-'
    return f'{fecha.day} DE {MESES[fecha.month - 1]} DEL {fecha.year}'


class ReportePDF:
    def __init__(self, titulo):
        self.buffer = io.BytesIO()
        self.ancho, self.alto = A4
        self.c = canvas.Canvas(self.buffer, pagesize=A4)
        self.titulo = titulo.upper()
        self.margen_x = 45
        self.inicio_contenido = self.alto - 240
        self.img = None
        plantilla = _ruta_plantilla()
        if plantilla.exists():
            self.img = ImageReader(str(plantilla))
            self.c.drawImage(self.img, 0, 0, width=self.ancho, height=self.alto, preserveAspectRatio=False, mask='auto')
        self.y = self.inicio_contenido

    def _nueva_pagina_si_necesario(self, minimo=200):
        if self.y < minimo:
            self.c.showPage()
            if self.img:
                self.c.drawImage(self.img, 0, 0, width=self.ancho, height=self.alto, preserveAspectRatio=False, mask='auto')
            self.y = self.alto - 200

    def encabezado(self, subtitulo=None):
        self.c.setFont('Helvetica-Bold', 16)
        self.c.drawCentredString(self.ancho / 2, self.y, self.titulo)
        self.y -= 28
        if subtitulo:
            self.c.setFont('Helvetica', 10)
            self.c.drawCentredString(self.ancho / 2, self.y, subtitulo)
            self.y -= 22
        hoy = timezone.localdate()
        self.c.setFont('Helvetica', 10)
        self.c.drawString(self.margen_x, self.y, f'Fecha de reporte: {_formatear_fecha(hoy)}')
        self.y -= 25

    def linea_info(self, etiqueta, valor):
        self._nueva_pagina_si_necesario(180)
        self.c.setFont('Helvetica-Bold', 10)
        self.c.drawString(self.margen_x, self.y, f'{etiqueta}:')
        self.c.setFont('Helvetica', 10)
        self.c.drawString(self.margen_x + 90, self.y, str(valor))
        self.y -= 16

    def tabla(self, encabezados, filas, anchos=None):
        ancho_tabla = self.ancho - (self.margen_x * 2)
        if not anchos:
            anchos = [ancho_tabla / len(encabezados)] * len(encabezados)

        self._nueva_pagina_si_necesario(220)
        self.c.setFillColor(colors.HexColor('#333333'))
        self.c.rect(self.margen_x, self.y - 5, ancho_tabla, 20, fill=1, stroke=0)
        self.c.setFillColor(colors.white)
        self.c.setFont('Helvetica-Bold', 9)
        x = self.margen_x + 5
        for i, enc in enumerate(encabezados):
            if i == len(encabezados) - 1:
                self.c.drawRightString(x + anchos[i] - 10, self.y, enc)
            else:
                self.c.drawString(x, self.y, enc)
            x += anchos[i]
        self.c.setFillColor(colors.black)
        self.y -= 24

        self.c.setFont('Helvetica', 9)
        for fila in filas:
            self._nueva_pagina_si_necesario(200)
            x = self.margen_x + 5
            for i, celda in enumerate(fila):
                texto = str(celda)[:50]
                if i == len(fila) - 1:
                    self.c.drawRightString(x + anchos[i] - 10, self.y, texto)
                else:
                    self.c.drawString(x, self.y, texto)
                x += anchos[i]
            self.c.setStrokeColor(colors.HexColor('#dddddd'))
            self.c.line(self.margen_x, self.y - 5, self.margen_x + ancho_tabla, self.y - 5)
            self.y -= 18

        if not filas:
            self.c.drawString(self.margen_x + 5, self.y, 'Sin registros para los filtros aplicados.')
            self.y -= 18

    def total(self, etiqueta, valor):
        self.y -= 8
        self.c.setFont('Helvetica-Bold', 11)
        self.c.drawRightString(self.ancho - self.margen_x - 90, self.y, f'{etiqueta}:')
        self.c.drawRightString(self.ancho - self.margen_x - 5, self.y, str(valor))
        self.y -= 20

    def nota(self, texto):
        if texto:
            self.y -= 10
            self.c.setFont('Helvetica-Bold', 8)
            self.c.drawCentredString(self.ancho / 2, self.y, f'NOTA: {texto.upper()}')

    def finalizar(self):
        self.c.save()
        self.buffer.seek(0)
        return self.buffer


def generar_pdf_ingresos(ingresos, total, filtros=None):
    pdf = ReportePDF('REPORTE DE INGRESOS')
    subtitulo = _subtitulo_filtros(filtros)
    pdf.encabezado(subtitulo)
    pdf.linea_info('Total ingresos', f'Bs. {total:.2f}')
    pdf.linea_info('Registros', len(ingresos))
    pdf.y -= 10
    filas = [
        [i.fecha.strftime('%d/%m/%Y'), i.concepto[:40], i.get_categoria_display(), str(i.cliente), f'{i.monto:.2f}']
        for i in ingresos
    ]
    pdf.tabla(['FECHA', 'CONCEPTO', 'CATEGORÍA', 'CLIENTE', 'MONTO BS'], filas, [70, 150, 90, 100, 70])
    pdf.total('Total', f'Bs. {total:.2f}')
    return pdf.finalizar()


def generar_pdf_egresos(egresos, total, filtros=None):
    pdf = ReportePDF('REPORTE DE EGRESOS')
    pdf.encabezado(_subtitulo_filtros(filtros))
    pdf.linea_info('Total egresos', f'Bs. {total:.2f}')
    pdf.linea_info('Registros', len(egresos))
    pdf.y -= 10
    filas = [
        [e.fecha.strftime('%d/%m/%Y'), e.concepto[:45], e.get_categoria_display(), f'{e.monto:.2f}']
        for e in egresos
    ]
    pdf.tabla(['FECHA', 'CONCEPTO', 'CATEGORÍA', 'MONTO BS'], filas, [80, 200, 120, 80])
    pdf.total('Total', f'Bs. {total:.2f}')
    return pdf.finalizar()


def generar_pdf_clientes(clientes, filtros=None):
    pdf = ReportePDF('REPORTE DE CLIENTES')
    pdf.encabezado(_subtitulo_filtros(filtros))
    pdf.linea_info('Total clientes', clientes.count())
    pdf.y -= 10
    filas = [
        [f'{c.nombre} {c.apellido}'.strip(), c.email or '-', c.telefono or '-',
         c.get_estado_display(), c.total_citas or 0, f'{c.total_ingresos or 0:.2f}']
        for c in clientes
    ]
    pdf.tabla(['NOMBRE', 'EMAIL', 'TELÉFONO', 'ESTADO', 'CITAS', 'INGRESOS BS'], filas, [110, 110, 70, 60, 45, 70])
    return pdf.finalizar()


def generar_pdf_citas(citas, filtros=None):
    pdf = ReportePDF('REPORTE DE CITAS')
    pdf.encabezado(_subtitulo_filtros(filtros))
    pdf.linea_info('Total citas', citas.count())
    pdf.y -= 10
    filas = [
        [f'{c.cliente}', c.fecha.strftime('%d/%m/%Y %H:%M'),
         str(c.empleado) if c.empleado else '-', f'{c.duracion_minutos} min', c.get_estado_display()]
        for c in citas
    ]
    pdf.tabla(['CLIENTE', 'FECHA', 'EMPLEADO', 'DURACIÓN', 'ESTADO'], filas, [120, 100, 100, 60, 70])
    return pdf.finalizar()


def generar_pdf_empleados(empleados, filtros=None):
    pdf = ReportePDF('REPORTE DE EMPLEADOS')
    pdf.encabezado(_subtitulo_filtros(filtros))
    pdf.linea_info('Total empleados', empleados.count())
    pdf.y -= 10
    filas = [
        [f'{e.nombre} {e.apellido}'.strip(), e.email or '-', e.telefono or '-',
         e.get_cargo_display(), e.get_estado_display(),
         e.total_citas or 0, e.total_eventos or 0, e.total_sesiones or 0]
        for e in empleados
    ]
    pdf.tabla(
        ['NOMBRE', 'EMAIL', 'TELÉFONO', 'CARGO', 'ESTADO', 'CITAS', 'EVENTOS', 'SESIONES'],
        filas, [90, 90, 65, 70, 55, 40, 50, 50],
    )
    return pdf.finalizar()


def generar_pdf_financiero(datos, filtros=None):
    pdf = ReportePDF('REPORTE FINANCIERO')
    pdf.encabezado(_subtitulo_filtros(filtros))
    pdf.linea_info('Total ingresos', f'Bs. {datos["total_ingresos"]:.2f}')
    pdf.linea_info('Total egresos', f'Bs. {datos["total_egresos"]:.2f}')
    pdf.linea_info('Saldo neto', f'Bs. {datos["saldo_neto"]:.2f}')
    pdf.linea_info('Pagos pendientes empleados', f'Bs. {datos["pagos_pendientes"]:.2f}')
    pdf.y -= 10
    filas = [
        ['Ingresos', f'Bs. {datos["total_ingresos"]:.2f}'],
        ['Egresos', f'Bs. {datos["total_egresos"]:.2f}'],
        ['Saldo neto', f'Bs. {datos["saldo_neto"]:.2f}'],
        ['Pagos pendientes', f'Bs. {datos["pagos_pendientes"]:.2f}'],
    ]
    pdf.tabla(['CONCEPTO', 'MONTO'], filas, [300, 120])
    return pdf.finalizar()


def _subtitulo_filtros(filtros):
    if not filtros:
        return None
    partes = []
    if filtros.get('fecha_inicio'):
        partes.append(f'Desde {filtros["fecha_inicio"]}')
    if filtros.get('fecha_fin'):
        partes.append(f'Hasta {filtros["fecha_fin"]}')
    if filtros.get('q'):
        partes.append(f'Búsqueda: {filtros["q"]}')
    if filtros.get('estado'):
        partes.append(f'Estado: {filtros["estado"]}')
    if filtros.get('categoria'):
        partes.append(f'Categoría: {filtros["categoria"]}')
    if filtros.get('cargo'):
        partes.append(f'Cargo: {filtros["cargo"]}')
    return ' | '.join(partes) if partes else 'Todos los registros'
