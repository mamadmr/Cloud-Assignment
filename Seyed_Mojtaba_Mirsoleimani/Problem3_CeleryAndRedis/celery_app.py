from celery import Celery

app = Celery('docker_tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1')
