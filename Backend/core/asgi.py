import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from notifications.middleware import JWTAuthMiddleware
from notifications.routing import (
    websocket_urlpatterns as notifications_websocket_urlpatterns,
)
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
websocket_urlpatterns = notifications_websocket_urlpatterns + chat_websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
