import docker
from celery_app import app

client = docker.from_env()

@app.task
def start_container(image_name):
    try:
        container = client.containers.run(image_name, detach=True)
        return container.id
    except Exception as e:
        return f"Error: {str(e)}"


@app.task
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Stopped container {container_id}"
    except Exception as e:
        return f"Error: {str(e)}"

