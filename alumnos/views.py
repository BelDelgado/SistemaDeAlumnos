from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Alumno
from .forms import AlumnoForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

@login_required
def dashboard(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    context = {
        'alumnos': alumnos
    }
    return render(request, 'alumnos/dashboard.html', context)

@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, f'Alumno {alumno.nombre_completo} creado exitosamente')
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm()
    
    return render(request, 'alumnos/crear_alumno.html', {'form': form, 'titulo': 'Crear Alumno'})

@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            messages.success(request, f'Alumno {alumno.nombre_completo} actualizado exitosamente')
            return redirect('alumnos:dashboard')
    else:
        form = AlumnoForm(instance=alumno)
    
    return render(request, 'alumnos/editar_alumno.html', {'form': form, 'titulo': 'Editar Alumno'})

@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        nombre = alumno.nombre_completo
        alumno.delete()
        messages.success(request, f'Alumno {nombre} eliminado exitosamente')
        return redirect('alumnos:dashboard')
    
    return render(request, 'alumnos/eliminar_alumno.html', {'alumno': alumno})

@login_required
def enviar_pdf(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, usuario=request.user)
    
    # Generar PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, height - 100, "Información del Alumno")
    
    # Datos del alumno
    p.setFont("Helvetica", 12)
    y = height - 150
    p.drawString(100, y, f"Nombre Completo: {alumno.nombre_completo}")
    y -= 30
    p.drawString(100, y, f"Email: {alumno.email}")
    y -= 30
    p.drawString(100, y, f"Teléfono: {alumno.telefono}")
    y -= 30
    p.drawString(100, y, f"Fecha de Nacimiento: {alumno.fecha_nacimiento}")
    y -= 30
    p.drawString(100, y, f"Dirección: {alumno.direccion}")
    y -= 30
    p.drawString(100, y, f"Fecha de Registro: {alumno.fecha_registro.strftime('%d/%m/%Y')}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    
    # Enviar por email
    email = EmailMessage(
        f'Información del Alumno: {alumno.nombre_completo}',
        f'Adjunto encontrarás la información del alumno {alumno.nombre_completo}.',
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email if request.user.email else alumno.email],
    )
    email.attach(f'alumno_{alumno.nombre}_{alumno.apellido}.pdf', buffer.getvalue(), 'application/pdf')
    
    try:
        email.send()
        messages.success(request, f'PDF enviado exitosamente a {request.user.email if request.user.email else alumno.email}')
    except Exception as e:
        messages.error(request, f'Error al enviar el email: {str(e)}')
    
    return redirect('alumnos:dashboard')