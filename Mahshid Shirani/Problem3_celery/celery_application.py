from celery import Celery

app = Celery('container_tasks', broker='redis://localhost:6379/0',
     backend='redis://localhost:6379/0')
# Optional: for better visibility of what's going on
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

