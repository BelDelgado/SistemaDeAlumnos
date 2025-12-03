from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER
import os
import csv
from django.conf import settings
from django.http import HttpResponse

def generar_pdf_alumno(alumno):
    """Genera un PDF con los datos del alumno"""
    
    # Crear directorio temporal si no existe
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    # Ruta del archivo PDF
    pdf_path = os.path.join(temp_dir, f'alumno_{alumno.id}.pdf')
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#7F8C8D'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Título
    title = Paragraph('Datos del Alumno', title_style)
    elements.append(title)
    
    # Fecha
    fecha_texto = f"Generado el: {alumno.fecha_registro.strftime('%d/%m/%Y %H:%M')}"
    subtitle = Paragraph(fecha_texto, subtitle_style)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.3*inch))
    
    # Datos del alumno en tabla
    data = [
        ['Campo', 'Información'],
        ['Nombre Completo', alumno.nombre_completo],
        ['Nombre', alumno.nombre],
        ['Apellido', alumno.apellido],
        ['Nota', str(alumno.nota)],
        ['Fecha de Registro', alumno.fecha_registro.strftime('%d/%m/%Y %H:%M')],
    ]
    
    table = Table(data, colWidths=[2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(table)
    
    # Pie de página
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#95A5A6'),
        alignment=TA_CENTER
    )
    footer = Paragraph('Sistema de Gestión de Alumnos', footer_style)
    elements.append(footer)
    
    # Construir PDF
    doc.build(elements)
    
    return pdf_path


def exportar_alumnos_csv(alumnos):
    """Genera un archivo CSV con la lista de alumnos"""
    
    # Crear la respuesta HTTP con el tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alumnos.csv"'
    
    # Crear el escritor CSV
    writer = csv.writer(response)
    
    # Escribir encabezados
    writer.writerow(['nombre', 'apellido', 'nota'])
    
    # Escribir datos de cada alumno
    for alumno in alumnos:
        writer.writerow([
            alumno.nombre,
            alumno.apellido,
            str(alumno.nota)
        ])
    
    return response