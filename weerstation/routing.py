from django.urls import re_path
from .consumers import SensorUpload, SensorReader, RegenSensorUpload

# WebSocket URL's en hun respectieve consumers
websocket_urlpatterns = [
    re_path(r'ws/upload/$', SensorUpload.as_asgi()),   # Consumer voor het ontvangen van sensor data en opslaan
    re_path(r'ws/liveSensorData/$', SensorReader.as_asgi()),   # Consumer voor het uitlezen van sensor data in realtime
    re_path(r'ws/regensensor/$', RegenSensorUpload.as_asgi()),
]
