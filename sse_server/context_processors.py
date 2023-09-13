import environ
from django.conf import settings


env = environ.Env()
environ.Env.read_env(settings.BASE_DIR / ".env")


def sse_server_url(_):
    return {"sse_server_url": env.str("SSE_SERVER_URL")}
