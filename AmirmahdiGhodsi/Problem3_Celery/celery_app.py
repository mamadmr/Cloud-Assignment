from celery import Celery

app = Celery(
    "tasks",
    broker="redis://redis:6379/0",   # talk to the redis service
    backend="redis://redis:6379/0"
)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    result_expires=3600,
)