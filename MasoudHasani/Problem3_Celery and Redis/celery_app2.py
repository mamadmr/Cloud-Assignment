from celery import Celery

app = Celery(
    'ctf_manager',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
from tasks import start_ctf_container, stop_ctf_container
