from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta

from .models import RegistroEntrenamiento
from .serializers import RegistroEntrenamientoSerializer

Usuario = get_user_model()

class RegistroEntrenamientoViewSet(viewsets.ModelViewSet):
    queryset = RegistroEntrenamiento.objects.all()
    serializer_class = RegistroEntrenamientoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtrar registros por usuario autenticado"""
        return self.queryset.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        """Asignar el usuario autenticado al crear un registro"""
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """
        Obtener entrenamientos de un usuario específico
        GET /api/entrenamientos/by_user/?user_id=1
        """
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'Se requiere el parámetro user_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que el usuario existe
        usuario = get_object_or_404(Usuario, id=user_id)

        # Obtener todos los entrenamientos del usuario
        entrenamientos = self.queryset.filter(usuario=usuario).select_related(
            'usuario',
            'rutina'
        )

        serializer = self.get_serializer(entrenamientos, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Obtener estadísticas de entrenamientos por diferentes períodos
        GET /api/entrenamientos/statistics/
        Parámetros opcionales:
        - period: 'dia', 'semana', 'mes', 'ano'
        - user_id: ID del usuario (opcional, por defecto el usuario autenticado)
        """
        # Determinar el usuario
        user_id = request.query_params.get('user_id')
        if user_id:
            usuario = get_object_or_404(Usuario, id=user_id)
        else:
            usuario = request.user

        # Determinar el período
        period = request.query_params.get('period', 'dia')
        now = timezone.now()

        # Definir el filtro de fecha según el período
        if period == 'dia':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'semana':
            start_date = now - timedelta(days=now.weekday())
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == 'mes':
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == 'ano':
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return Response(
                {'error': 'Período inválido. Usa dia, semana, mes o ano'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtrar entrenamientos
        entrenamientos = RegistroEntrenamiento.objects.filter(
            usuario=usuario,
            fecha__gte=start_date
        )

        # Calcular estadísticas
        stats = {
            'total_entrenamientos': entrenamientos.count(),
            'entrenamientos_por_rutina': list(
                entrenamientos.values('rutina__nombre')
                .annotate(count=Count('id'))
                .order_by('-count')
            ),
            'periodo': period,
            'fecha_inicio': start_date,
        }

        return Response(stats)