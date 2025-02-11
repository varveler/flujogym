from django.db import models
from django.conf import settings


class GrupoMuscular(models.TextChoices):
    PIERNAS = 'piernas', 'Piernas'
    PECHO = 'pecho', 'Pecho'
    ESPALDA = 'espalda', 'Espalda'
    HOMBROS = 'hombros', 'Hombros'
    BRAZOS = 'brazos', 'Brazos'
    ABDOMINALES = 'abdominales', 'Abdominales'
    FULLBODY = 'fullbody', 'Full Body'


class Ejercicio(models.Model):
    nombre = models.CharField('Nombre del ejercicio', max_length=100)
    descripcion = models.TextField('Descripción')
    grupo_muscular = models.CharField(
        'Grupo muscular',
        max_length=50,
        choices=GrupoMuscular.choices,
        default=GrupoMuscular.FULLBODY
    )
    equipamiento_necesario = models.CharField('Equipamiento necesario', max_length=200, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_grupo_muscular_display()})"


class NivelDificultad(models.TextChoices):
    PRINCIPIANTE = 'principiante', 'Principiante'
    INTERMEDIO = 'intermedio', 'Intermedio'
    AVANZADO = 'avanzado', 'Avanzado'


class Rutina(models.Model):
    nombre = models.CharField('Nombre de la rutina', max_length=100)
    descripcion = models.TextField('Descripción')
    nivel_dificultad = models.CharField(
        'Nivel de dificultad',
        max_length=20,
        choices=NivelDificultad.choices,
        default=NivelDificultad.PRINCIPIANTE
    )
    duracion_estimada = models.PositiveIntegerField('Duración estimada (minutos)')
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rutinas_creadas')
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_nivel_dificultad_display()}"


class EjercicioEnRutina(models.Model):
    rutina = models.ForeignKey(Rutina,on_delete=models.CASCADE, related_name='ejercicios')
    ejercicio = models.ForeignKey(Ejercicio,on_delete=models.CASCADE)
    orden = models.PositiveIntegerField('Orden')
    series = models.PositiveIntegerField('Número de series')
    repeticiones = models.CharField('Repeticiones', max_length=50)
    descanso = models.PositiveIntegerField('Descanso (segundos)')

    class Meta:
        ordering = ['orden']
        unique_together = [['rutina', 'orden']]

    def __str__(self):
        return f"{self.ejercicio.nombre} - Serie {self.orden}"


class DiaSemana(models.TextChoices):
    LUNES = 'LUN', 'Lunes'
    MARTES = 'MAR', 'Martes'
    MIERCOLES = 'MIE', 'Miércoles'
    JUEVES = 'JUE', 'Jueves'
    VIERNES = 'VIE', 'Viernes'
    SABADO = 'SAB', 'Sábado'
    DOMINGO = 'DOM', 'Domingo'


class ProgramacionRutina(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='programaciones')
    rutina = models.ForeignKey( 'Rutina', on_delete=models.CASCADE, related_name='programaciones')
    dia_semana = models.CharField('Día de la semana',max_length=3,choices=DiaSemana.choices,default=DiaSemana.LUNES)
    hora = models.TimeField('Hora de la rutina', null=True, blank=True)
    activa = models.BooleanField('Programación activa', default=True)

    class Meta:
        ordering = ['dia_semana', 'hora']
        unique_together = [['usuario', 'dia_semana']]

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.rutina.nombre} - {self.get_dia_semana_display()}"