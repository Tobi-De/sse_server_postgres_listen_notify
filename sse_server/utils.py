import json

from django.db import connection


def postgres_notify(channel_name: str, sse_event: dict):
    with connection.cursor() as cursor:
        cursor.execute(f"NOTIFY {channel_name}, '{json.dumps(sse_event)}'")
