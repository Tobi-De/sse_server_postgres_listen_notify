import json

from django.db import connection


def postgres_notify(channel: str, sse_payload: dict):
    with connection.cursor() as cursor:
        cursor.execute(f"NOTIFY {channel}, '{json.dumps(sse_payload)}'")
