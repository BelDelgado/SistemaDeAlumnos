from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Alumno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alumnos')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, verbose_name='Apellido')
    nota = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Nota',
        help_text='Nota del alumno (0-10)'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')

    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'