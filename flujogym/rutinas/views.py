from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Ejercicio, Rutina, EjercicioEnRutina
from .serializers import EjercicioSerializer, RutinaSerializer, EjercicioEnRutinaSerializer

class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer

class EjercicioEnRutinaViewSet(viewsets.ModelViewSet):
    queryset = EjercicioEnRutina.objects.all()
    serializer_class = EjercicioEnRutinaSerializer


class RutinaViewSet(viewsets.ModelViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar rutinas por usuario autenticado"""
        return self.queryset.filter(creada_por=self.request.user)

    def perform_create(self, serializer):
        """Asignar el usuario autenticado como creador de la rutina"""
        serializer.save(creada_por=self.request.user)

    @action(detail=True, methods=['post'])
    def agregar_ejercicio(self, request, pk=None):
        """
        Agregar un ejercicio a la rutina.
        Ejemplo del payload:
        {
            "ejercicio_id": 1,
            "orden": 1,
            "series": 4,
            "repeticion": "12",
            "descanso": 90
        }
        """
        rutina = self.get_object()
        ejercicio = get_object_or_404(Ejercicio, pk=request.data.get('ejercicio_id'))

        # Validar que el ejercicio no esté ya en la rutina
        if EjercicioEnRutina.objects.filter(rutina=rutina, ejercicio=ejercicio).exists():
            return Response(
                {'detail': 'Este ejercicio ya está en la rutina'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ejercicio_en_rutina = EjercicioEnRutina.objects.create(
            rutina=rutina,
            ejercicio=ejercicio,
            orden=request.data.get('orden'),
            series=request.data.get('series'),
            repeticiones=request.data.get('repeticiones'),
            descanso=request.data.get('descanso')
        )

        serializer = EjercicioEnRutinaSerializer(ejercicio_en_rutina)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def ejercicios(self, request, pk=None):
        """Obtener todos los ejercicios de una rutina"""
        rutina = self.get_object()
        ejercicios = EjercicioEnRutina.objects.filter(rutina=rutina).order_by('orden')
        serializer = EjercicioEnRutinaSerializer(ejercicios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['delete'])
    def eliminar_ejercicio(self, request, pk=None):
        """
        Eliminar un ejercicio de la rutina
        Se debe enviar el ejercicio_id en la URL:
        DELETE /api/rutinas/{rutina_id}/eliminar_ejercicio/?ejercicio_id={ejercicio_id}
        """
        rutina = self.get_object()
        ejercicio_id = request.query_params.get('ejercicio_id')

        if not ejercicio_id:
            return Response(
                {'detail': 'Debe especificar el ejercicio_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        ejercicio_en_rutina = get_object_or_404(
            EjercicioEnRutina,
            rutina=rutina,
            ejercicio_id=ejercicio_id
        )
        ejercicio_en_rutina.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)