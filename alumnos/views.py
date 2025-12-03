from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings
from .models import Alumno
from .forms import AlumnoForm
from .utils import generar_pdf_alumno, exportar_alumnos_csv
import os

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/dashboard.html', {'alumnos': alumnos})

@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, f'Alumno {alumno.nombre_completo} creado exitosamente.')
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm()
    
    return render(request, 'alumnos/crear_alumno.html', {'form': form})

@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, f'Alumno {alumno.nombre_completo} actualizado exitosamente.')
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm(instance=alumno)
    
    return render(request, 'alumnos/editar_alumno.html', {'form': form, 'alumno': alumno})

@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        nombre = alumno.nombre_completo
        alumno.delete()
        messages.success(request, f'Alumno {nombre} eliminado exitosamente.')
        return redirect('alumnos:dashboard')
    
    return render(request, 'alumnos/eliminar_alumno.html', {'alumno': alumno})

@login_required
def generar_pdf_alumno_view(request, pk):
    """Genera y descarga el PDF del alumno"""
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    try:
        # Generar PDF
        pdf_path = generar_pdf_alumno(alumno)
        
        # Abrir el archivo PDF
        pdf_file = open(pdf_path, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="alumno_{alumno.nombre}_{alumno.apellido}.pdf"'
        
        messages.success(request, f'PDF de {alumno.nombre_completo} generado exitosamente.')
        
        # Eliminar archivo temporal después de un tiempo
        # (Django lo manejará automáticamente después de enviar la respuesta)
        
        return response
        
    except Exception as e:
        messages.error(request, f'Error al generar el PDF: {str(e)}')
        return redirect('alumnos:dashboard')

@login_required
def exportar_csv_view(request):
    """Exporta todos los alumnos del usuario a CSV"""
    alumnos = Alumno.objects.filter(usuario=request.user)
    
    if not alumnos.exists():
        messages.warning(request, 'No tienes alumnos para exportar.')
        return redirect('alumnos:dashboard')
    
    try:
        response = exportar_alumnos_csv(alumnos)
        messages.success(request, f'Se exportaron {alumnos.count()} alumnos exitosamente.')
        return response
    except Exception as e:
        messages.error(request, f'Error al exportar CSV: {str(e)}')
        return redirect('alumnos:dashboard')