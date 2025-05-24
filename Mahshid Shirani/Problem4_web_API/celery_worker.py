from celery import Celery

celery_app = Celery(
    "ctf_tasks",
    broker="redis://localhost:6379/0",  # or your Redis container URL
    backend="redis://localhost:6379/0"
)
