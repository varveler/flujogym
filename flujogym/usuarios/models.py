from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=True)
    telefono = models.CharField('Teléfono', max_length=15, blank=True)
    direccion = models.TextField('Dirección', blank=True)

    fecha_inscripcion = models.DateField('Fecha de inscripción', auto_now_add=True)
    activo = models.BooleanField('¿Usuario activo?', default=True)

    def __str__(self):
        return f"{self.get_full_name()} - {"Activo" if self.esta_activo else "Inactivo"}"