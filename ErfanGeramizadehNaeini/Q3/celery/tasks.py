from celery import Celery
import os
import docker


app = Celery(
    'tasks',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://redis:6390/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://redis:6390/0'),
)

client = docker.from_env()


@app.task(name='tasks.add')  # just for test
def add(x, y):
    return x + y


@app.task(name='tasks.start')
def start_container(image_name, container_name=None):
    try:
        container = client.containers.run(
            image=image_name,
            name=container_name,
            detach=True
        )
        return f"{container.id}"
    except docker.errors.APIError as e:
        return f"Error starting container: {str(e)}"


@app.task(name='tasks.stop')
def stop_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Container {container_id} stopped"
    except docker.errors.NotFound:
        return f"Container {container_id} not found"
    except docker.errors.APIError as e:
        return f"Error stopping container: {str(e)}"
