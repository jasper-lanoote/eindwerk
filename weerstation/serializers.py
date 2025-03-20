from rest_framework import serializers
from .models import SensorData
from .models import RegenMeting

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ['id', 'timestamp', 'temperature', 'humidity', 'pressure', 'gas', 'wind_speed_kmh']

class RegenMetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegenMeting
        fields = ['id', 'tijdstip', 'regenval']
