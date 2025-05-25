import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctfsystem.settings')

app = Celery('CTF',
            broker='redis://redis:6379/0',  
            backend='redis://redis:6379/0',
             include=['api.tasks'])  

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.imports = ['api.tasks']
app.autodiscover_tasks()
