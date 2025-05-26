from celery import Celery

celery_app = Celery(
    "container_manager",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

celery_app.conf.update(
    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",
    timezone="Asia/Tehran",
    task_track_started=True,
)
