from rest_framework import serializers
from .models import RegistroEntrenamiento

class RegistroEntrenamientoSerializer(serializers.ModelSerializer):
    rutina_nombre = serializers.CharField(source='rutina.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = RegistroEntrenamiento
        fields = (
            'id', 'usuario', 'usuario_nombre',
            'rutina', 'rutina_nombre',
            'fecha', 'completado'
        )
        read_only_fields = ('usuario', 'fecha')