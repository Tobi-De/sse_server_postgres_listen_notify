import json

import environ
import psycopg
from django.db import connection
from sse_starlette.sse import EventSourceResponse, ServerSentEvent
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.routing import Route

env = environ.Env()


async def event_publisher(req: Request):
    connection_params = connection.get_connection_params()
    connection_params.pop("cursor_factory")
    aconnection = await psycopg.AsyncConnection.connect(
        **connection_params,
        autocommit=True,
    )
    channel = req.query_params.get("channel")
    if not channel:
        return

    async with aconnection.cursor() as acursor:
        await acursor.execute(f"LISTEN {channel}")
        generator = aconnection.notifies()
        async for notify_message in generator:
            yield ServerSentEvent(**json.loads(notify_message.payload))


async def sse(request: Request):
    return EventSourceResponse(event_publisher(request))


routes = [Route("/", endpoint=sse)]


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=env.list("SSE_ALLOWED_ORIGINS"),
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
]

app = Starlette(debug=env("DJANGO_DEBUG"), routes=routes, middleware=middleware)
