import docker
from celery_app import app


# Initialize Docker client
client = docker.from_env()


@app.task
def start_container(image_name):
    try:
        container = client.containers.run(image=image_name, detach=True)
        return f"Container started with ID: {container.id}"
    except Exception as e:
        return f"Error starting container: {str(e)}"


@app.task
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Container with ID {container_id} stopped."
    except Exception as e:
        return f"Error stopping container: {str(e)}"
