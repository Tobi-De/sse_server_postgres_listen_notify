import uvicorn
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help_text = "Run uvicorn server to handle server sent events requests"

    def add_arguments(self, parser):
        parser.add_argument(
            "--host",
            type=str,
            default="0.0.0.0",
            help="server host",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=8001,
            help="server port",
        )

        parser.add_argument("--workers", type=int)

    def handle(self, *args, **options):
        uvicorn.run(
            "smartestate.sse_server.asgi_app:app",
            host=options.get("host"),
            port=options.get("port"),
            reload=settings.DEBUG,
            workers=options.get("workers"),
        )
