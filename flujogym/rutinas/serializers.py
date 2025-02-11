from rest_framework import serializers
from .models import Ejercicio, Rutina, EjercicioEnRutina, ProgramacionRutina


class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'


class EjercicioEnRutinaSerializer(serializers.ModelSerializer):
    ejercicio_nombre = serializers.CharField(source='ejercicio.nombre', read_only=True)
    ejercicio_descripcion = serializers.CharField(source='ejercicio.descripcion', read_only=True)
    grupo_muscular = serializers.CharField(source='ejercicio.grupo_muscular', read_only=True)

    class Meta:
        model = EjercicioEnRutina
        fields = (
            'id', 'rutina', 'ejercicio', 'orden', 'series', 'repeticiones', 'descanso',
            'ejercicio_nombre', 'ejercicio_descripcion', 'grupo_muscular'
        )


class RutinaSerializer(serializers.ModelSerializer):
    ejercicios = EjercicioEnRutinaSerializer(many=True, read_only=True)
    creada_por_username = serializers.CharField(source='creada_por.username', read_only=True)
    total_ejercicios = serializers.SerializerMethodField()
    total_minutos = serializers.SerializerMethodField()

    class Meta:
        model = Rutina
        fields = (
            'id', 'nombre', 'descripcion', 'nivel_dificultad',
            'duracion_estimada', 'creada_por', 'creada_por_username',
            'fecha_creacion', 'ejercicios', 'total_ejercicios', 'total_minutos'
        )
        read_only_fields = ('creada_por', 'fecha_creacion')

    def get_total_ejercicios(self, obj):
        return obj.ejercicios.count()

    def get_total_minutos(self, obj):
        total_seconds = 0
        for ejercicio in obj.ejercicios.all():
            # Tiempo por serie, asumiendo 30 segundos por set de repeticiones
            tiempo_por_serie = 30
            # Tiempo total del ejercicio considerando descanso
            total_seconds += (tiempo_por_serie + ejercicio.descanso) * ejercicio.series
        return total_seconds // 60


class ProgramacionRutinaSerializer(serializers.ModelSerializer):
    rutina_nombre = serializers.CharField(source='rutina.nombre', read_only=True)
    dia_semana_display = serializers.CharField(source='get_dia_semana_display', read_only=True)

    class Meta:
        model = ProgramacionRutina
        fields = (
            'id', 'usuario', 'rutina', 'rutina_nombre',
            'dia_semana', 'dia_semana_display', 'hora', 'activa'
        )
        read_only_fields = ('usuario',)