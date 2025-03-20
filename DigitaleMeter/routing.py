from django.urls import path
from . import consumers
from .consumers import DigitaleMeterConsumer
websocket_urlpatterns = [
path('ws/sc/', consumers.MySyncConsumer.as_asgi()),
path('ws/ac/', consumers.MyAsyncConsumer.as_asgi()),
path('ws/digitalemeter/', consumers.DigitaleMeterConsumer.as_asgi()),
]