from app.celery_app import celery_app


import app.tasks

app = celery_app

