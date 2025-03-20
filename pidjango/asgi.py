import os
 
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import weerstation.routing
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "pidjango.settings")
 
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(weerstation.routing.websocket_urlpatterns)
})