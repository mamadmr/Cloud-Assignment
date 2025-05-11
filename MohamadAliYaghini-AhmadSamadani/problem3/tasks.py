from celery import Celery
import docker
from celery.exceptions import SoftTimeLimitExceeded

# Configure Celery with Redis as the broker
app = Celery(
    'ctf_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Initialize Docker client
docker_client = docker.from_env()

@app.task(bind=True, soft_time_limit=30, time_limit=40)
def start_container(self, image_name, container_name):
    try:
        # Check if container already exists
        try:
            existing_container = docker_client.containers.get(container_name)
            if existing_container.status == 'running':
                return f"Container {container_name} is already running."
            else:
                existing_container.start()
                return f"Container {container_name} started."
        except docker.errors.NotFound:
            # Create and start new container
            container = docker_client.containers.run(
                image_name,
                name=container_name,
                detach=True
            )
            return f"Container {container_name} created and started with ID {container.id}."
    except SoftTimeLimitExceeded:
        return f"Task to start {container_name} timed out."
    except Exception as e:
        return f"Error starting container {container_name}: {str(e)}"

@app.task(bind=True, soft_time_limit=30, time_limit=40)
def stop_container(self, container_name):
    try:
        container = docker_client.containers.get(container_name)
        container.stop()
        return f"Container {container_name} stopped."
    except docker.errors.NotFound:
        return f"Container {container_name} not found."
    except SoftTimeLimitExceeded:
        return f"Task to stop {container_name} timed out."
    except Exception as e:
        return f"Error stopping container {container_name}: {str(e)}"
