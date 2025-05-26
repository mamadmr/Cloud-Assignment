from celery import Celery

app = Celery('ctf_tasks', broker='redis://redis:6379/0')

app.conf.update(
    result_backend='redis://redis:6379/0',
    task_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)
