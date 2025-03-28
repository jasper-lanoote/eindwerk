import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from weerstation.routing import websocket_urlpatterns  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pidjango.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Normale HTTP-verzoeken
    "websocket": AuthMiddlewareStack(  # WebSocket-verbindingen
        URLRouter(
            websocket_urlpatterns  # Verbind de WebSocket-URL's met de juiste consumers
        )
    ),
})
