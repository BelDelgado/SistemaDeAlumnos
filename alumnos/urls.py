from django.urls import path
from . import views

app_name = 'alumnos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('editar/<int:pk>/', views.editar_alumno, name='editar_alumno'),
    path('eliminar/<int:pk>/', views.eliminar_alumno, name='eliminar_alumno'),
    path('generar-pdf/<int:pk>/', views.generar_pdf_alumno_view, name='generar_pdf_alumno'),
    path('exportar-csv/', views.exportar_csv_view, name='exportar_csv'),
]