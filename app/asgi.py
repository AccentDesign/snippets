import os

from django.core.asgi import get_asgi_application
from uvicorn.workers import UvicornWorker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
app = get_asgi_application()


class DjangoUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"lifespan": "off"}
