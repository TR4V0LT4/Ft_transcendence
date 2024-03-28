from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from ludo.consumers import Fconsumer
from django.core.asgi import get_asgi_application

websocket_urlpatterns = [
    path('ws/ludo/game/', Fconsumer.as_asgi()),
    # Add more WebSocket URL patterns as needed
]
# websocket_urlpatterns = [
#     re_path(r'ws/ludo/game/$', Fconsumer.as_asgi()),
# ]
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})