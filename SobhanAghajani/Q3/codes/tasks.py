import docker
from celery_app import app

client = docker.from_env()


@app.task
def start_container(image_name, container_name=None):
    try:
        container = client.containers.run(
            image_name,
            name=container_name,
            detach=True
        )
        return f"Started container: {container.id}"
    except Exception as e:
        return f"Error starting container: {str(e)}"


@app.task
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Stopped container: {container_id}"
    except Exception as e:
        return f"Error stopping container: {str(e)}"
