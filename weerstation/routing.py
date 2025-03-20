from django.urls import path
from .consumers import SensorConsumer

websocket_urlpatterns = [
    path("ws/sensoren/", SensorConsumer.as_asgi()), #addres in postman: ws://192.168.0.232:8000/ws/sensoren/

]
