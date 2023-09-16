 # sse_server_postgres_listen_notify

> **Update**: I've made a package (and a docker image) out of this https://github.com/Tobi-De/sse_relay_server

This project has one main goal: to grab events from PostgreSQL and shoot them straight to your browser using Server-Sent Events (SSE). It's like an alternative route compared to what's explained [here](https://valberg.dk/django-sse-postgresql-listen-notify.html). Instead of diving deep into async views and the new StreamingHttpResponse from Django 4.2, we use a Starlette application to handle sse connections. In my experience, it's more stable and just as easy to set up. Plus, it keeps our Django project free from the async mess.

Just a heads up, this is best suited for simpler tasks. If you're planning some fancy, complex business logic (especially if it involves Django models) around the sse stuff, this is probably not what you need.

**Note**:
This is not a package; you should copy-paste the code and adapt it for your project. Depending on where you paste the code source for the app, you may need to update some paths:
- In `sse_server/management/commands/sse_serve.py`, make sure you update `sse_server.asgi_app:app` to `myproject.sse_server.asgi_app:app` within the uvicorn path.
- Also, in `sse_server/apps.py`, change sse_server to `myproject.sse_server` in the app_name property.


## Requirements

- [uvicorn](https://www.uvicorn.org/)
- [starlette[standard]](https://www.starlette.io/)
- [sse-starlette](https://github.com/sysid/sse-starlette)
- [psycopg](https://www.psycopg.org/psycopg3/)
- [django-environ](https://github.com/joke2k/django-environ)

## Environment Variables

```sh
SSE_SERVER_URL= # URL where the SSE server is running
SSE_ALLOWED_ORIGINS= # List of domains allowed to send SSE connection requests
```

## SSE Setup on the Frontend

This example uses the [htmx SSE extension](https://htmx.org/extensions/server-sent-events/).

```html
<div hx-ext="sse" 
    sse-connect="{{sse_server_url}}/?channel={{ postgres_sse_channel }}">
</div>
```

**channel**: The name of the PostgreSQL channel for listening to messages.

## Running the SSE Server

```sh
python manage.py sse_serve
```

## Sending Events from Your Django App

```python
from sse_server.utils import postgres_notify

postgres_notify(
    channel="Notifications",
    sse_payload={
        "event": "NEW_NOTIFICATION",
        "id": 1,
        "data": json.dumps({"message": "A new notification"}),
    },
)
```

**channel**: The PostgreSQL channel to use for sending the message (The same you specified in the template above).

**sse_payload**: A Python dictionary containing all the details of the SSE event. For a complete list of available options, refer to [this class definition](https://github.com/sysid/sse-starlette/blob/main/sse_starlette/sse.py#L50).

To keep things running smoothly, it's a good idea to avoid using overly lengthy channel names, excessively large payloads for postgre `notify messages`, and excessively bulky data for SSE event payloads, as there are size limitations for each of these aspects. If you find yourself needing to retrieve a hefty database object, consider sending just the key and fetching the full data on the frontend using another request (such as an htmx request). While this extra request may not be the most ideal solution, for simplicity's sake it's often a worthwhile trade-off.
At my workplace, we implemented a straightforward real-time notification system using this approach, successfully transmitting all the necessary notification data without any issues. However, it's essential to be aware of the potential risk of sending overly large data. For more in-depth information, you can refer to the following links:

- [Postgres Notify](https://www.postgresql.org/docs/15/sql-notify.html)
- [Postgres Listen](https://www.postgresql.org/docs/current/sql-listen.html)
- [Server Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)


## Optional: sse_server_url Context Processor

If you need the `sse_server_url` in every template, you can use the context processor as follows:

```python
# settings.py
TEMPLATES = [
    {
        ...,
        "OPTIONS": {
            "context_processors": [
                ...,
                "sse_server.context_processors.sse_server_url",
            ],
        },
    },
]
```
