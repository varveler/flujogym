from django.contrib import admin
from .models import Ejercicio, Rutina, EjercicioEnRutina, ProgramacionRutina


@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'grupo_muscular', 'equipamiento_necesario')
    list_filter = ('grupo_muscular',)
    search_fields = ('nombre', 'descripcion')


class EjercicioEnRutinaInline(admin.TabularInline):
    model = EjercicioEnRutina
    extra = 1
    ordering = ('orden',)


@admin.register(Rutina)
class RutinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_dificultad', 'duracion_estimada', 'creada_por', 'fecha_creacion')
    list_filter = ('nivel_dificultad', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion', 'creada_por__username')
    inlines = [EjercicioEnRutinaInline]
    readonly_fields = ('fecha_creacion',)


@admin.register(ProgramacionRutina)
class ProgramacionRutinaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rutina', 'dia_semana', 'hora', 'activa')
    list_filter = ('dia_semana', 'activa', 'usuario')
    search_fields = ('usuario__username', 'rutina__nombre')
    raw_id_fields = ('usuario', 'rutina')

    def get_queryset(self, request):
        # Optimizacion con select_related
        return super().get_queryset(request).select_related('usuario', 'rutina')


@admin.register(EjercicioEnRutina)
class EjercicioEnRutinaAdmin(admin.ModelAdmin):
    list_display = ('rutina', 'ejercicio', 'orden', 'series', 'repeticiones')
    list_filter = ('rutina', 'ejercicio')
    search_fields = ('rutina__nombre', 'ejercicio__nombre')
    ordering = ('rutina', 'orden')




