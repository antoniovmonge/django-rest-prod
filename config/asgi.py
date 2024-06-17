import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taxi.settings")

django_asgi_application = get_asgi_application()

from core.trips.consumers import TaxiConsumer  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": URLRouter(
            [
                path("taxi/", TaxiConsumer.as_asgi()),
            ],
        ),
    },
)
