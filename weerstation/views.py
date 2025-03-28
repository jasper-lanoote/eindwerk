from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import viewsets

from .serializers import RegenMetingSerializer
from .serializers import SensorDataSerializer

from .models import RegenMeting
from .models import SensorData


class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

class RegenMetingViewSet(viewsets.ModelViewSet):
    queryset = RegenMeting.objects.all()
    serializer_class = RegenMetingSerializer