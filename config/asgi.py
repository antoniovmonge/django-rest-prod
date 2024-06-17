import os

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
    },
)
