import docker
from celery_application import app

client = docker.from_env()

@app.task(bind=True)
def start_container(self, image_name, container_name=None):
    try:
        container = client.containers.run(
            image=image_name,
            name=container_name,
            detach=True,
            auto_remove=False
        )
        return f"Started container {container.id}"
    except Exception as e:
        self.retry(exc=e, countdown=5, max_retries=3)
        return str(e)

@app.task(bind=True)
def stop_container(self, container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return f"Stopped container {container_id}"
    except Exception as e:
        self.retry(exc=e, countdown=5, max_retries=3)
        return str(e)
