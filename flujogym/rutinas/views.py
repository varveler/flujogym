from rest_framework import viewsets
from .models import Ejercicio, Rutina, EjercicioEnRutina
from .serializers import EjercicioSerializer, RutinaSerializer, EjercicioEnRutinaSerializer

class EjercicioViewSet(viewsets.ModelViewSet):
    queryset = Ejercicio.objects.all()
    serializer_class = EjercicioSerializer

class RutinaViewSet(viewsets.ModelViewSet):
    queryset = Rutina.objects.all()
    serializer_class = RutinaSerializer

class EjercicioEnRutinaViewSet(viewsets.ModelViewSet):
    queryset = EjercicioEnRutina.objects.all()
    serializer_class = EjercicioEnRutinaSerializer