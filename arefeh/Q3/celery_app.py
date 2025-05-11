# celery_app.py

from celery import Celery

app = Celery('ctf_tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')
