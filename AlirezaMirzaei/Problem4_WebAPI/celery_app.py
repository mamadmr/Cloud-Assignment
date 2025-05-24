from dotenv import load_dotenv
import os
from celery import Celery

# Load .env from project root
load_dotenv()

# Broker and backend URLs from environment
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis-server:6379/0")
CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND", "redis://redis-server:6379/1"
)

# Include the task modules so Celery registers them
celery_app = Celery(
    "ctf_manager",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks"],
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)
