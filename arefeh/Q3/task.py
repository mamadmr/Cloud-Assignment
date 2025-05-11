# tasks.py

from celery_app import app
import docker

client = docker.from_env()

@app.task
def start_ctf_container(image_name):
    container = client.containers.run(image_name, detach=True)
    return f"Started container with ID: {container.id}"

@app.task
def stop_ctf_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    return f"Stopped container with ID: {container_id}"
