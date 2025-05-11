from celery_app import app
import docker

client = docker.from_env()

@app.task(bind=True, name="start_container")
def start_container(self, image_name, container_name):
    try:
        container = client.containers.run(
            image_name,
            name=container_name,
            detach=True
        )
        return container.id
    except docker.errors.APIError as exc:
        self.retry(exc=exc, countdown=5, max_retries=3)

@app.task(bind=True, name="stop_container")
def stop_container(self, container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return f"{container_name} stopped & removed"
    except docker.errors.NotFound:
        return f"{container_name} not found"