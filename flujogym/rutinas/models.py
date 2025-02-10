from django.db import models
from django.conf import settings


class Ejercicio(models.Model):
    nombre = models.CharField('Nombre del ejercicio', max_length=100)
    descripcion = models.TextField('Descripción')
    grupo_muscular = models.CharField(
        'Grupo muscular',
        max_length=50,
        choices=[
            ('piernas', 'Piernas'),
            ('pecho', 'Pecho'),
            ('espalda', 'Espalda'),
            ('hombros', 'Hombros'),
            ('brazos', 'Brazos'),
            ('abdominales', 'Abdominales'),
            ('fullbody', 'Full Body'),
        ]
    )
    equipamiento_necesario = models.CharField('Equipamiento necesario', max_length=200, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_grupo_muscular_display()})"


class Rutina(models.Model):
    nombre = models.CharField('Nombre de la rutina', max_length=100)
    descripcion = models.TextField('Descripción')
    nivel_dificultad = models.CharField(
        'Nivel de dificultad',
        max_length=20,
        choices=[
            ('principiante', 'Principiante'),
            ('intermedio', 'Intermedio'),
            ('avanzado', 'Avanzado'),
        ]
    )
    duracion_estimada = models.PositiveIntegerField('Duración estimada (minutos)')
    creada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rutinas_creadas'
    )
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_nivel_dificultad_display()}"


class EjercicioEnRutina(models.Model):
    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name='ejercicios'
    )
    ejercicio = models.ForeignKey(
        Ejercicio,
        on_delete=models.CASCADE
    )
    orden = models.PositiveIntegerField('Orden')
    series = models.PositiveIntegerField('Número de series')
    repeticiones = models.CharField('Repeticiones', max_length=50)
    descanso = models.PositiveIntegerField('Descanso (segundos)')

    class Meta:
        ordering = ['orden']
        unique_together = [['rutina', 'orden']]

    def __str__(self):
        return f"{self.ejercicio.nombre} - Serie {self.orden}"