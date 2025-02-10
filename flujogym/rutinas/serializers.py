from rest_framework import serializers
from .models import Ejercicio, Rutina, EjercicioEnRutina


class EjercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ejercicio
        fields = '__all__'


class EjercicioEnRutinaSerializer(serializers.ModelSerializer):
    ejercicio_nombre = serializers.CharField(source='ejercicio.nombre', read_only=True)

    class Meta:
        model = EjercicioEnRutina
        fields = '__all__'


class RutinaSerializer(serializers.ModelSerializer):
    ejercicios = EjercicioEnRutinaSerializer(many=True, read_only=True)

    class Meta:
        model = Rutina
        fields = '__all__'