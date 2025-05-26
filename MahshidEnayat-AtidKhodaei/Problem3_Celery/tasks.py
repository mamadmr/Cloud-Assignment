from celery import Celery
from docker_utils import start_ctf_container, stop_ctf_container

app = Celery('ctf_tasks')
app.config_from_object('celeryconfig')

@app.task
def start_container_task(image_name, container_name, port_map=None):
    return start_ctf_container(image_name, container_name, port_map)

@app.task
def stop_container_task(container_id):
    return stop_ctf_container(container_id)