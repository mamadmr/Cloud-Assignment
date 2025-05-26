from workers.celery_instance import celery_app
import docker

client = docker.from_env()

@celery_app.task(bind=True)
def launch_container(self, image_name, container_name, host_port=None, container_port=None):
    try:
        ports = None
        if host_port:
            ports = {f"{container_port}/tcp": host_port}

        container = client.containers.run(
            image_name,
            name=container_name,
            detach=True,
            ports=ports
        )
        return container.id
    except docker.errors.APIError as exc:
        self.retry(exc=exc, countdown=5, max_retries=3)

@celery_app.task(bind=True)
def terminate_container(self, container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return f"{container_name} stopped and removed"
    except docker.errors.NotFound:
        return f"{container_name} not found"
