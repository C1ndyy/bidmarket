import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import main_app.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bid.settings")

application = ProtocolTypeRouter({
  "https": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            main_app.routing.websocket_urlpatterns
        )
    ),
})