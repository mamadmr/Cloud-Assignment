from celery import Celery

# Redis hostname is from docker-compose service name
REDIS_URL = "redis://redis:6379/0"

celery = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery.conf.task_routes = {
    "app.tasks.start_container": {"queue": "containers"},
    "app.tasks.stop_container": {"queue": "containers"},
}

