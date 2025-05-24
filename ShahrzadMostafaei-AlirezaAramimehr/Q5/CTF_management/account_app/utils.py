import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CTF_management.settings')

app = Celery('CTF',
            broker='redis://my-redis:6379/0',  
            backend='redis://my-redis:6379/0',
             include=['account_app.tasks'])  

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.imports = ['account_app.tasks']
app.autodiscover_tasks()

