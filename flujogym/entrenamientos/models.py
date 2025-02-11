from django.db import models
from django.conf import settings
from rutinas.models import Rutina

class RegistroEntrenamiento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registros_entrenamientos'
    )
    rutina = models.ForeignKey(
        Rutina,
        on_delete=models.CASCADE,
        related_name='registros'
    )
    fecha = models.DateTimeField(
        'Fecha y hora del entrenamiento',
        auto_now_add=True
    )
    completado = models.BooleanField(
        'Entrenamiento completado',
        default=True
    )

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Registro de entrenamiento'
        verbose_name_plural = 'Registros de entrenamientos'

    def __str__(self):
        return f"{self.usuario.username} - {self.rutina.nombre} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"