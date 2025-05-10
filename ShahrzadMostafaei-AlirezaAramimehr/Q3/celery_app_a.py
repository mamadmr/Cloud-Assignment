# celery_app.py
from celery import Celery

app = Celery('ctf_container_management', broker='redis://localhost:6379/0')

@app.task
def test_task():
    return 'Celery is working!'
