from celery import Celery

REDIS_URL = "redis://redis:6379/0"

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.task_routes = {
    "app.tasks.start_container": {"queue": "containers"},
    "app.tasks.stop_container": {"queue": "containers"},
}

