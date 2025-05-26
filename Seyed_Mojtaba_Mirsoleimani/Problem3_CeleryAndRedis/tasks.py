import docker
from celery_app import app

client = docker.from_env()

@app.task
def start_container(image_name, ports=None):
    container = client.containers.run(image_name, detach=True, ports=ports)
    return container.id

@app.task
def stop_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    return f"Container {container_id} stopped"
