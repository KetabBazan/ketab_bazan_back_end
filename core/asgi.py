"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path
from django.urls import re_path
from channels.auth import AuthMiddlewareStack

from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# conversa_dj directory.
from chat.views import ChatRoomView

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(ROOT_DIR / "conversa_dj"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

# This application object is used by any ASGI server configured to use this file.
django_application = get_asgi_application()

# Import websocket application here, so apps from django_application are loaded first

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa isort:skip

websocket_urlpatterns = [
    re_path(
        r"ws/chat/(?P<group_id>\w+)$", ChatRoomView.as_asgi()
    ),
]

application = ProtocolTypeRouter(
    {
        "websocket": URLRouter(websocket_urlpatterns),
    }
)
