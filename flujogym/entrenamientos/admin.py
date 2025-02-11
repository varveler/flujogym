from django.contrib import admin
from .models import RegistroEntrenamiento


@admin.register(RegistroEntrenamiento)
class RegistroEntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'fecha', 'completado')
    list_filter = ('fecha', 'completado', 'usuario', 'rutina')
    search_fields = ('usuario__username', 'rutina__nombre')
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)