from celery import Celery

celery = Celery(
    "ctf_manager",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.autodiscover_tasks(['app'])

import app.tasks