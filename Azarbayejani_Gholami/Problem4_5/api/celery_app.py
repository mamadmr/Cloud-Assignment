from celery import Celery

celery = Celery(
    'ctf_tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

